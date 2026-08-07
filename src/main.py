import src.functions as f
import src.globals as g
import supervisely as sly
from supervisely.convert.volume.nii.nii_planes_volume_converter import (
    NiiPlaneStructuredAnnotationConverter,
)

# * 1. Get project and dataset infos
try:
    project = g.api.project.get_info_by_id(g.project_id)
    if project is None:
        raise Exception(f"Project with id={g.project_id} not found")
    labeling_interface = f.get_labeling_interface(project)
    dataset = None
    dataset_created = False
    project_created_by_importer = False
    if g.dataset_id:
        dataset = g.api.dataset.get_info_by_id(g.dataset_id)
    if dataset is None:
        dataset = g.api.dataset.create(project.id, g.dataset_name, change_name_if_conflict=True)
        dataset_created = True
    g.dataset_id = dataset.id
    g.project_modality = project.type
except Exception as e:
    f.handle_exception_and_stop(e, "Error occurred. Please, contact support")


# * 2. initialize importer to detect format
try:
    if g.input_paths is None:
        raise Exception("Please, provide data to import.")
    importer = sly.ImportManager(
        g.input_paths,
        g.project_modality,
        labeling_interface=labeling_interface,
        upload_as_links=g.import_as_links,
    )
except Exception as e:
    if not f.is_no_modality_items_error(e):
        f.handle_exception_and_stop(e, "Format was not recognized")
    sly.logger.info(
        "No modality items detected for the selected project. "
        "Attempting to autodetect modality and format."
    )
    try:
        autodetected_importer = f.autodetect_importer(
            g.input_paths,
            g.import_as_links,
            excluded_modality=g.project_modality,
        )
    except Exception as autodetect_exc:
        f.handle_exception_and_stop(autodetect_exc, "Format was not recognized")

    if autodetected_importer is None:
        f.handle_exception_and_stop(e, "Format was not recognized")

    importer = autodetected_importer

    if dataset_created:
        sly.logger.info("Cleaning up unused dataset...")
        g.api.dataset.remove(g.dataset_id)
        sly.logger.info(f"Dataset '{dataset.name}' was removed. ")

    project, dataset = f.create_project_and_dataset(
        importer.modality,
        g.dataset_name,
        g.input_paths,
    )
    g.project_modality = project.type
    g.dataset_id = dataset.id
    dataset_created = True
    labeling_interface = f.get_labeling_interface(project)
    sly.logger.info(
        "Autodetected modality and created a new project. "
        f"Project: '{project.name}' (ID: {project.id}), "
        f"Dataset: '{dataset.name}' (ID: {dataset.id})."
    )

# * 3 Convert and upload data
try:
    new_dataset_id = importer.upload_dataset(g.dataset_id)
    if new_dataset_id is not None:
        project_created_by_importer = True
except Exception as e:
    f.handle_exception_and_stop(e, "Failed to convert and upload data. Please, check the logs")


if hasattr(importer.converter, "blob_project") and importer.converter.blob_project:
    sly.logger.info(
        "Data was uploaded in blob format. "
        "All items have been added to the top level of the project. "
    )
    if dataset_created:
        sly.logger.info("Cleaning up unused dataset...")
        g.api.dataset.remove(g.dataset_id)
        sly.logger.info(f"Dataset '{dataset.name}' was removed. ")
    output_title = f"{project.name}"
else:
    prefix_parts = []
    if dataset_created:
        prefix_parts.append("New ")
    if project_created_by_importer:
        g.dataset_id = new_dataset_id
        dataset = g.api.dataset.get_info_by_id(g.dataset_id)
        project = g.api.project.get_info_by_id(dataset.project_id)
        sly.logger.info("New project and dataset were created during import process.")
        sly.logger.info(f"Project: '{project.name}' (ID: {project.id})")
        sly.logger.info(f"Dataset: '{dataset.name}' (ID: {dataset.id})")
    if "dataset" not in dataset.name.lower():
        prefix_parts.append("Dataset: ")

    prefix = "".join(prefix_parts)
    output_title = f"{project.name}. {prefix}{dataset.name}".strip()

if isinstance(importer.converter, NiiPlaneStructuredAnnotationConverter):
    if dataset_created:
        sly.logger.info("Cleaning up unused dataset...")
        g.api.dataset.remove(g.dataset_id)
        sly.logger.info(f"Dataset '{dataset.name}' was removed. ")

# * 4. Set output project
g.api.task.set_output_project(g.task_id, project.id, output_title)
g.workflow.add_output(project)

# * 5. Clean app_data directory
sly.fs.clean_dir(g.app_data)
