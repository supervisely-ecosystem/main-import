import src.globals as g
import supervisely as sly


def handle_exception_and_stop(exc: Exception, msg: str = "Error"):
    from supervisely.io.exception_handlers import (
        handle_exception as sly_handle_exception,
    )

    handled_exc = sly_handle_exception(exc)
    if handled_exc is not None:
        g.api.task.set_output_error(g.task_id, handled_exc.title, handled_exc.message)
        handled_exc.log_error_for_agent()
    else:
        err_msg = repr(exc)
        if len(err_msg) > 255:
            err_msg = err_msg[:252] + "..."
        g.api.task.set_output_error(g.task_id, msg, err_msg)
        sly.logger.error(f"{msg}. {repr(exc)}")
    sly.logger.info(
        f"Debug info:\n"
        f"    team_id={g.team_id}\n    workspace_id={g.workspace_id}\n"
        f"    project_id={g.project_id}\n    dataset_id={g.dataset_id}\n"
        f"    project_modality={g.project_modality}\n    src_dir={g.src_dir}\n"
    )
    sly.fs.clean_dir(g.app_data)
    exit(0)
