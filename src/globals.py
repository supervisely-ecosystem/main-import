import datetime
import os

from distutils.util import strtobool
from dotenv import load_dotenv

import supervisely as sly
from supervisely.collection.str_enum import StrEnum

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()

app_data = sly.app.get_data_dir()
sly.fs.clean_dir(app_data)

task_id = sly.env.task_id()
team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()
project_id = sly.env.project_id()
dataset_id = sly.env.dataset_id(raise_not_found=False)

import_as_links = bool(strtobool(os.environ.get("modal.state.importAsLinks", "false")))
default_ds_name = f"dataset {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
dataset_name = os.environ.get("modal.state.datasetName", default_ds_name)
if dataset_name == "":
    dataset_name = default_ds_name
existing_ds_names = set([ds.name for ds in api.dataset.get_list(project_id, recursive=True)])
dataset_name = sly.generate_free_name(existing_ds_names, dataset_name, False, True)

input_path = sly.env.folder(raise_not_found=False)
if input_path is None:
    input_path = sly.env.file(raise_not_found=False)

project_modality = None


class LabelingInterfaces(StrEnum):
    DEFAULT = "default"
    MULTI_VIEW = "multi_view"
    MULTISPECTRAL = "multispectral"
    MEDICAL_2D = "medical_imaging_single"
    HIGH_COLOR = "images_with_16_color"
