import os

from dotenv import load_dotenv

import src.functions as f
import supervisely as sly

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))


app_data = sly.app.get_data_dir()
sly.fs.clean_dir(app_data)
api = sly.Api()

try:
    task_id = sly.env.task_id()
    team_id = sly.env.team_id()
    workspace_id = sly.env.workspace_id()
    project_id = sly.env.project_id()
    dataset_id = sly.env.dataset_id(raise_not_found=False)
    dataset_name = os.environ.get("modal.state.datasetName", "ds0")
    src_dir = sly.env.folder()

    # * 1. Get project and dataset infos
    project = api.project.get_info_by_id(project_id)
    if dataset_id:
        dataset = api.dataset.get_info_by_id(dataset_id)
    else:
        dataset = api.dataset.create(project.id, dataset_name, change_name_if_conflict=True)

    project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))
    project_modality = project.type
except Exception as e:
    sly.fs.clean_dir(app_data)
    f.handle_exception(e, "Error occurred. Please, contact support.")


try:
    # * 2. initialize importer
    importer = sly.ImportManager(src_dir, project_modality)
except Exception as e:
    sly.fs.clean_dir(app_data)
    f.handle_exception(e, "Failed to detect format. Please, check the input data.")

try:
    # * 3 Convert and upload
    importer.upload_dataset(dataset.id)
except Exception as e:
    sly.fs.clean_dir(app_data)
    f.handle_exception(e, "Failed to convert and upload data. Please, check the logs.")

# * 4. Set output project
output_title = f"{project.name}. New dataset: {dataset.name}"
api.task.set_output_project(task_id, project.id, output_title)

# * 5. Clean app_data directory
sly.fs.clean_dir(app_data)


# TODO list:
# - [ ] self._annotations – check if it is necessary (or remove it)
# - [ ] global var MODALITY, optimize detect_modality
# - [ ] configure convenient module import (ex: import supervisely.convert.image.COCOFORMAT)
# - [ ] rename file converter.py? rename class ImportManager?
# - [ ] rename images (items) if exists in the dataset (while uploading)
