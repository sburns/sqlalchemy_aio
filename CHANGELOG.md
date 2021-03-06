# Change Log
## [Unreleased][unreleased]
### Added
- `AsyncConnection.dialect` property.
- `AsyncEngine.sync_engine` property.
- `AsyncConnection.sync_connection`property.
- Blocking method `run_callable` has been implemented for
  `AsyncConnection` and `AsyncEngine`. This allows
  `Table(..., autoload_with=engine)`, which emits a `BlockingWarning`.
- Detects attempts to use `Table().create(bind=engine)` or
  `MetaData().create_all()` and raises a helpful error message.
- Detects attempts to use `MetData().reflect()` and raises a helpful
  error message.
- `AsyncConnection.connect()` method.
- Public `run_in_thread()` async method has been added to `AsyncConnection`
  and `AsyncEngine`.

### Fixed
- `ThreadWorker.quit()` will raise `AlreadyQuit` instead of blocking.
  This is only called internally.
- Connections created using `AsyncEngine.begin()` now create their own
  worker, like `AsyncEngine.connect()`.

## [0.13.0][0.13.0]
### Added
- [Trio] support with `TRIO_STRATEGY`.

### Changed
- A new `ThreadWorker` class is used internally to defer work to instead
  of using a `ThreadPoolExecutor`.

[Trio]: https://github.com/python-trio/trio

## [0.12.0] - 2018-02-06
### Added
- `AsyncioResultProxy.fetchmany`
- `AsyncioResultProxy.__aiter__`

## [0.11.0] - 2017-03-12
### Added
- `AsyncioEngine.scalar()`
- `AsyncioConnection.scalar()`

### Fixed
- Connections now get their own thread. Now threadsafe DBAPI modules are more
  useful without passing a custom executor as in 0.10.0

### Changed
- **Backwards incompatible:** removed `executor` argument, since the engine
  takes care of threads now.


## [0.10.0] - 2016-12-19
Initial release.

[unreleased]: https://github.com/RazerM/sqlalchemy_aio/compare/0.13.0...HEAD
[0.13.0]: https://github.com/RazerM/sqlalchemy_aio/compare/0.12.0...0.13.0
[0.12.0]: https://github.com/RazerM/sqlalchemy_aio/compare/0.11.0...0.12.0
[0.11.0]: https://github.com/RazerM/sqlalchemy_aio/compare/0.10.0...0.11.0
[0.10.0]: https://github.com/RazerM/sqlalchemy_aio/compare/458d37d8...0.10.0
