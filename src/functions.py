import src.globals as g
import supervisely as sly


def get_labeling_interface(project: sly.ProjectInfo) -> str:
    import_settings = project.import_settings
    if not import_settings or not isinstance(import_settings, dict):
        import_settings = {"labelingInterface": "default", "computerVisionTask": "universal"}
    return import_settings.get("labelingInterface", "default")

def handle_exception_and_stop(exc: Exception, msg: str = "Error"):
    from supervisely.io.exception_handlers import (
        handle_exception as sly_handle_exception,
    )

    debug_info = {
        "team_id": g.team_id,
        "workspace_id": g.workspace_id,
        "project_id": g.project_id,
        "dataset_id": g.dataset_id,
        "project_modality": g.project_modality,
        "src_dir": g.input_path,
    }

    handled_exc = sly_handle_exception(exc)
    if handled_exc is not None:
        g.api.task.set_output_error(g.task_id, handled_exc.title, handled_exc.message)
        err_msg = handled_exc.get_message_for_exception()
        sly.logger.error(err_msg, extra=debug_info, exc_info=True)
    else:
        err_msg = repr(exc)
        if len(err_msg) > 255:
            err_msg = err_msg[:252] + "..."
        g.api.task.set_output_error(g.task_id, msg, err_msg)
        sly.logger.error(f"{msg}. {repr(exc)}", extra=debug_info, exc_info=True)
    sly.fs.clean_dir(g.app_data)
    exit(0)
