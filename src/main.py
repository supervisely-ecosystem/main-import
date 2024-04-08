import supervisely as sly

import src.functions as f
import src.globals as g

# * 1. Get project and dataset infos
try:
    project = g.api.project.get_info_by_id(g.project_id)
    if g.dataset_id:
        dataset = g.api.dataset.get_info_by_id(g.dataset_id)
    else:
        dataset = g.api.dataset.create(project.id, g.dataset_name, change_name_if_conflict=True)
    project_modality = project.type
except Exception as e:
    f.handle_exception_and_stop(e, "Error occurred. Please, contact support.")


# * 2. initialize importer to detect format
try:
    importer = sly.ImportManager(g.src_dir, project_modality)
except Exception as e:
    f.handle_exception_and_stop(e, "Failed to detect format. Please, check the input data.")

# * 3 Convert and upload data
try:
    importer.upload_dataset(dataset.id)
except Exception as e:
    f.handle_exception_and_stop(e, "Failed to convert and upload data. Please, check the logs.")

# * 4. Set output project
output_title = f"{project.name}. New dataset: {dataset.name}"
g.api.task.set_output_project(g.task_id, project.id, output_title)

# * 5. Clean app_data directory
sly.fs.clean_dir(g.app_data)
