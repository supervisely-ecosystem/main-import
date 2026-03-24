import datetime
import os
import subprocess

from dotenv import load_dotenv

import supervisely as sly
from workflow import Workflow

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()
workflow = Workflow(api)

try:
    _sly_version = subprocess.check_output(
        ["pip", "show", "supervisely"], text=True, stderr=subprocess.DEVNULL
    )
    _sly_version = next(
        (line.split(": ", 1)[1].strip() for line in _sly_version.splitlines() if line.startswith("Version:")),
        "unknown",
    )
except Exception:
    _sly_version = "unknown"
sly.logger.info(f"Supervisely SDK version: {_sly_version}")

app_data = sly.app.get_data_dir()
sly.fs.clean_dir(app_data)

task_id = sly.env.task_id()
team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()
project_id = sly.env.project_id()
dataset_id = sly.env.dataset_id(raise_not_found=False)

import_as_links = (os.environ.get("modal.state.importAsLinks", "false")).lower() == "true"
default_ds_name = f"dataset {datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}"
dataset_name = os.environ.get("modal.state.datasetName", default_ds_name)
if dataset_name == "":
    dataset_name = default_ds_name
existing_ds_names = set([ds.name for ds in api.dataset.get_list(project_id, recursive=True)])
dataset_name = sly.generate_free_name(existing_ds_names, dataset_name, False, True)

input_paths = sly.env.folders(raise_not_found=False) or sly.env.folder(raise_not_found=False)
if input_paths is None:
    input_paths = sly.env.files(raise_not_found=False) or sly.env.file(raise_not_found=False)


project_modality = None
