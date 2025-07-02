import src.globals as g
import supervisely as sly
from supervisely.io.exception_handlers import ErrorHandler
from supervisely.project.project_settings import LabelingInterface
from supervisely.project.project_type import _MULTISPECTRAL_TAG_NAME


def get_project_settings(project_id: int) -> sly.ProjectSettings:
    project_meta = sly.ProjectMeta.from_json(g.api.project.get_meta(project_id))
    return project_meta.project_settings


def get_labeling_interface(project: sly.ProjectInfo) -> str:
    project_settings = get_project_settings(project.id)
    import_settings = project.import_settings
    labeling_interface = None
    if import_settings and isinstance(import_settings, dict):
        labeling_interface = import_settings.get("labelingInterface")
    if labeling_interface is None:
        if not project_settings.multiview_enabled:
            labeling_interface = LabelingInterface.DEFAULT
        elif project_settings.multiview_tag_name == _MULTISPECTRAL_TAG_NAME:
            labeling_interface = LabelingInterface.MULTISPECTRAL
        else:
            labeling_interface = LabelingInterface.MULTIVIEW
    return labeling_interface


def handle_exception_and_stop(exc: Exception, msg: str = "Error"):
    from supervisely.io.exception_handlers import (
        handle_exception as sly_handle_exception,
    )

    sly.fs.clean_dir(g.app_data)

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
        err_msg = handled_exc.get_message_for_exception()
        sly.logger.error(err_msg, extra=debug_info, exc_info=True)
        if isinstance(handled_exc, ErrorHandler.API.PaymentRequired):
            raise exc
        else:
            g.api.task.set_output_error(g.task_id, handled_exc.title, handled_exc.message)
    else:
        err_msg = repr(exc)
        if len(err_msg) > 255:
            err_msg = err_msg[:252] + "..."
        g.api.task.set_output_error(g.task_id, msg, err_msg)
        exc_str = str(exc) if isinstance(exc, RuntimeError) else repr(exc)  # for better logging
        sly.logger.error(f"{msg}. {exc_str}", extra=debug_info, exc_info=True)
    exit(0)
