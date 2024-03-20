import os

from dotenv import load_dotenv

import supervisely as sly

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()

app_data = sly.app.get_data_dir()
sly.fs.clean_dir(app_data)

api = sly.Api()

task_id = sly.env.task_id()
team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()
project_id = sly.env.project_id()
dataset_id = sly.env.dataset_id(raise_not_found=False)
dataset_name = os.environ.get("modal.state.datasetName", "ds0")
src_dir = sly.env.folder()
project_modality = None
