import trio
import threading
from functools import partial

import outcome
from trio import Cancelled, RunFinishedError

from .base import AsyncEngine, ThreadWorker
from .exc import AlreadyQuit

_STOP = object()


class TrioThreadWorker(ThreadWorker):
    def __init__(self, *, branch_from=None):
        if branch_from is None:
            self._portal = trio.BlockingTrioPortal()
            self._request_queue = trio.Queue(1)
            self._response_queue = trio.Queue(1)
            self._thread = threading.Thread(target=self.thread_fn, daemon=True)
            self._thread.start()
        else:
            self._portal = branch_from._portal
            self._request_queue = branch_from._request_queue
            self._response_queue = branch_from._response_queue
            self._thread = branch_from._thread

        self._branched = branch_from is not None
        self._has_quit = False

    def thread_fn(self):
        while True:
            try:
                request = self._portal.run(self._request_queue.get)
            except Cancelled:
                continue
            except RunFinishedError:
                break

            if request is not _STOP:
                response = outcome.capture(request)
                self._portal.run(self._response_queue.put, response)
            else:
                self._portal.run(self._response_queue.put, None)
                break

    async def run(self, func, args=(), kwargs=None):
        if self._has_quit:
            raise AlreadyQuit

        if kwargs:
            func = partial(func, *args, **kwargs)
        elif args:
            func = partial(func, *args)

        await self._request_queue.put(func)
        resp = await self._response_queue.get()
        return resp.unwrap()

    async def quit(self):
        if self._has_quit:
            raise AlreadyQuit

        self._has_quit = True

        if self._branched:
            return

        await self._request_queue.put(_STOP)
        await self._response_queue.get()


class TrioEngine(AsyncEngine):
    """Mostly like :class:`sqlalchemy.engine.Engine` except some of the methods
    are coroutines."""
    def _make_worker(self, *, branch_from=None):
        return TrioThreadWorker(branch_from=branch_from)
