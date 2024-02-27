import os

from dotenv import load_dotenv

import supervisely as sly
from supervisely.convert.converter import ImportManager

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))


app_data = sly.app.get_data_dir()
sly.fs.clean_dir(app_data)
api = sly.Api()


workspace_id = sly.env.workspace_id()
team_id = sly.env.team_id()
project_id = sly.env.project_id()
dataset_id = sly.env.dataset_id(raise_not_found=False)
task_id = sly.env.task_id()
dataset_name = os.environ.get("datasetName", "ds0")

src_dir = sly.env.folder()


# * 1. Get project and dataset infos
project = api.project.get_info_by_id(project_id)
if dataset_id:
    dataset = api.dataset.get_info_by_id(dataset_id)
else:
    dataset = api.dataset.create(project.id, dataset_name, change_name_if_conflict=True)

project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))
project_modality = project.type


# * 2. initialize importer
importer = ImportManager(src_dir, project_modality)

# * 3 Convert and upload
importer.upload_dataset(dataset.id)

# * 4. Set output project
api.task.set_output_project(task_id, project.id)

# * 5. Clean app_data directory
sly.fs.clean_dir(app_data)


# TODO list:
# - [ ] self._annotations – check if it is necessary (or remove it)
# - [ ] global var MODALITY, optimize detect_modality
# - [ ] configure convenient module import (ex: import supervisely.convert.image.COCOFORMAT)
# - [ ] rename file converter.py? rename class ImportManager?
# - [ ] rename images (items) if exists in the dataset (while uploading)
