import supervisely as sly


def handle_exception(exc: Exception, msg: str = "Error"):
    from supervisely.io.exception_handlers import (
        handle_exception as sly_handle_exception,
    )

    handled_exc = sly_handle_exception(exc)
    if handled_exc is not None:
        handled_exc.log_error_for_agent()
    else:
        sly.logger.error(f"{msg}. {repr(exc)}")
    exit(0)
