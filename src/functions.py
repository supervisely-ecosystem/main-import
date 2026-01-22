import os
from datetime import datetime

import src.globals as g
import supervisely as sly
from supervisely.io.exception_handlers import ErrorHandler
from supervisely.project.project_settings import LabelingInterface
from supervisely.project.project_type import _MULTISPECTRAL_TAG_NAME, ProjectType


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
        "input_paths": g.input_paths,
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


def is_no_modality_items_error(exc: Exception) -> bool:
    msg = str(exc)
    return (
        "Not found any" in msg
        or "Please refer to the app overview" in msg
        or "Unsupported file extensions detected" in msg
    )


def _default_project_name(input_paths) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    if isinstance(input_paths, (list, tuple)):
        if len(input_paths) == 1:
            base = os.path.basename(str(input_paths[0]).rstrip("/"))
        else:
            base = timestamp
    else:
        base = os.path.basename(str(input_paths).rstrip("/"))
    if base == "":
        base = timestamp

    existing_names = {p.name for p in g.api.project.get_list(g.workspace_id)}
    return sly.generate_free_name(existing_names, base, False, True)


def create_project_and_dataset(
    modality: ProjectType, dataset_name: str, input_paths
) -> tuple[sly.ProjectInfo, sly.DatasetInfo]:
    project_name = _default_project_name(input_paths)
    project = g.api.project.create(
        g.workspace_id,
        project_name,
        change_name_if_conflict=True,
        type=modality,
    )
    dataset = g.api.dataset.create(project.id, dataset_name, change_name_if_conflict=True)
    return project, dataset


def autodetect_importer(
    input_paths,
    upload_as_links: bool,
    excluded_modality: ProjectType = None,
) -> sly.ImportManager:
    detected_importers = []
    for modality in ProjectType:
        if excluded_modality is not None and str(modality) == str(excluded_modality):
            continue
        try:
            importer = sly.ImportManager(
                input_paths,
                modality,
                labeling_interface=LabelingInterface.DEFAULT,
                upload_as_links=upload_as_links,
            )
        except Exception as e:
            sly.logger.debug(f"Autodetect failed for modality {modality}: {repr(e)}")
            continue
        if importer.converter.items_count == 0:
            continue
        detected_importers.append(importer)

    if len(detected_importers) == 0:
        return None
    if len(detected_importers) > 1:
        raise RuntimeError(
            "Multiple modalities detected: "
            f"{[str(i.modality) for i in detected_importers]}. "
            "Please split your data and try again."
        )
    return detected_importers[0]
