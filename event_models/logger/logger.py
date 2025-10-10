import logging
from typing import override, Any

from event_models.logger.message import LoggerMessage

from fluent.handler import FluentHandler, FluentRecordFormatter  # type: ignore[import-untyped]


class AppLogger(logging.Logger):
    def __init__(self, name: str) -> None:
        super().__init__(name)

        self._logger = logging.getLogger(name)

    @staticmethod
    def init_fluent_logging(tag: str, host: str, port: int, log_format: str, datefmt: str) -> None:
        fluent_handler = FluentHandler(
            tag=tag,
            host=host,
            port=port,
            nanosecond_precision=True,
        )

        formatter = SafeFluentRecordFormatter(
            {
                "log": log_format,
                "level": "%(levelname)s",
                "message_id": "%(message_id)s",
            }
        )

        formatter.datefmt = datefmt
        fluent_handler.setFormatter(formatter)
        fluent_handler.setLevel(logging.DEBUG)

        logger = logging.getLogger()
        logger.addHandler(fluent_handler)

    @override
    def debug(
        self,
        msg: object,
        *args: object,
        message_id: Any = LoggerMessage.UNKNOWN,
        exc_info: Any = None,
        stack_info: Any = False,
        stacklevel: int = 1,
        extra: Any = None,
    ) -> None:
        if extra:
            extra["message_id"] = str(message_id)
        else:
            extra = {"message_id": str(message_id)}

        self._logger.debug(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    @override
    def info(
        self,
        msg: object,
        *args: object,
        message_id: Any = LoggerMessage.UNKNOWN,
        exc_info: Any = None,
        stack_info: Any = False,
        stacklevel: int = 1,
        extra: Any = None,
    ) -> None:
        if extra:
            extra["message_id"] = str(message_id)
        else:
            extra = {"message_id": str(message_id)}

        self._logger.info(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    @override
    def warning(
        self,
        msg: object,
        *args: object,
        message_id: Any = LoggerMessage.UNKNOWN,
        exc_info: Any = None,
        stack_info: Any = False,
        stacklevel: int = 1,
        extra: Any = None,
    ) -> None:
        if extra:
            extra["message_id"] = str(message_id)
        else:
            extra = {"message_id": str(message_id)}

        self._logger.warning(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    @override
    def error(
        self,
        msg: object,
        *args: object,
        message_id: Any = LoggerMessage.UNKNOWN,
        exc_info: Any = None,
        stack_info: Any = False,
        stacklevel: int = 1,
        extra: Any = None,
    ) -> None:
        if extra:
            extra["message_id"] = str(message_id)
        else:
            extra = {"message_id": str(message_id)}

        self._logger.error(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    @override
    def critical(
        self,
        msg: object,
        *args: object,
        message_id: Any = LoggerMessage.UNKNOWN,
        exc_info: Any = None,
        stack_info: Any = False,
        stacklevel: int = 1,
        extra: Any = None,
    ) -> None:
        if extra:
            extra["message_id"] = str(message_id)
        else:
            extra = {"message_id": str(message_id)}

        self._logger.critical(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    @override
    def exception(
        self,
        msg: object,
        *args: object,
        message_id: Any = LoggerMessage.UNKNOWN,
        exc_info: Any = True,
        stack_info: Any = False,
        stacklevel: int = 1,
        extra: Any = None,
    ) -> None:
        if extra:
            extra["message_id"] = str(message_id)
        else:
            extra = {"message_id": str(message_id)}

        self._logger.exception(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )


class FluentLoggerWriter:
    def __init__(self, level: Any) -> None:
        self.level = level
        self._buffer = ""

    def write(self, message: str) -> None:
        if message.strip():
            self.level(message.strip())

    def flush(self) -> None:
        pass


class SafeFluentRecordFormatter(FluentRecordFormatter):  # type: ignore[misc]
    def format(self, record: Any) -> str:
        if not hasattr(record, "message_id"):
            record.message_id = str(LoggerMessage.UNKNOWN)

        return super().format(record)  # type: ignore[no-any-return]
