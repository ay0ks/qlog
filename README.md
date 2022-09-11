# QLog

## Example:
-----

```py
import qlog

log = qlog.QLog(log_level=qlog.QLevel.Debug)
app = qlog.QLogId(1, "App")

log.trace(app, "test")
log.debug(app, "test")
log.info(app, "test")
log.warn(app, "test")
log.error(app, "test")
log.critical(app, "test")
```

