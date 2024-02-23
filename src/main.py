import os

from dotenv import load_dotenv

import supervisely as sly

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))


api = sly.Api()


workspace_id = sly.env.workspace_id()
project_id = sly.env.project_id(raise_not_found=False)
dataset_id = sly.env.dataset_id(raise_not_found=False)
project_modality = os.getenv("PROJECT_MODALITY")
src_dir = os.getenv("SRC_DIR")

if not src_dir:
    raise RuntimeError("SRC_DIR is not specified.")
if not project_modality:
    raise RuntimeError("PROJECT_MODALITY is not specified.")
elif project_modality not in sly.ProjectType:
    raise RuntimeError("PROJECT_MODALITY is not valid.")


# * 1. Get project and dataset infos

if dataset_id:
    dataset = api.dataset.get_info_by_id(dataset_id)
    project = api.project.get_info_by_id(dataset.project_id)
else:
    if project_id:
        project = api.project.get_info_by_id(project_id)
    else:
        project = api.project.create(
            workspace_id,
            "Imported Project",
            change_name_if_conflict=True,
            type=project_modality,
        )
    dataset = api.dataset.create(project.id, "ds0", change_name_if_conflict=True)
project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))


# * 2. initialize importer
importer = sly.ImportManager(src_dir, project_modality)

# * 3 Convert and upload
importer.upload_dataset(dataset.id)

# TODO list:
# - [ ] self._annotations – check if it is necessary (or remove it)
# - [ ] global var MODALITY, optimize detect_modality
# - [ ] configure convenient module import (ex: import supervisely.convert.image.COCOFORMAT)
# - [ ] rename file converter.py? rename class ImportManager?
# - [ ] rename images (items) if exists in the dataset (while uploading)
