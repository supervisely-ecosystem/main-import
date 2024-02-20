import os

from dotenv import load_dotenv

import supervisely as sly

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))


api = sly.Api()

team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()
project_id = sly.env.project_id(raise_not_found=False)
dataset_id = sly.env.dataset_id(raise_not_found=False)

project_modality = sly.ProjectType.IMAGES  # sly.env.project_modality()


src_dir = "data" # "video" # "pcd"

importer = sly.ImportManager(src_dir, project_modality)

if project_id is None:
    project = api.project.create(
        workspace_id,
        "new converted data",
        change_name_if_conflict=True,
        type=project_modality,
    )
    project_id = project.id

if dataset_id is None:
    dataset = api.dataset.create(
        project_id, "converted data ds", change_name_if_conflict=True
    )
    dataset_id = dataset.id


importer.upload_dataset(dataset_id)


# steps:
# 1. importer creates a converter
# 2. converter detecting format (in validate_format)
# 3. get necessary info from input dir
# 3.1. count annotations (validate_format returns False if 0)
# 3.2. attempting to find key file and validate it
# 3.3. iterate over files and folders in the input dirs to create list of images and dict with anns {file_name: path}
# 3.4. read existing ProjectMeta or create empty ProjectMeta
# 4. converter create items
# 4.1. create Item with path to image
# 4.2. attempting to match Item.name to ann_dict keys
# 4.3. if ann_data is found, validate it, if success, add ann_data to Item
# 4.3. if self._meta doesn't exist, generate meta from annotation and update meta from each found annotation
# 4.4. add created Item to self._items
# 4.5 count detected annotations
# 5. validate_format method should return True or False based on detected annotations count


# validate_format:
# - prepare meta
# - update self._items with items (match annotation if exists)
# - return True if annotations found, False if not
