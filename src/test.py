import os

from dotenv import load_dotenv

import supervisely as sly
from supervisely.convert.converter import ImportManager

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))


api = sly.Api()

team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()
project_id = sly.env.project_id(raise_not_found=False)
if project_id is None:
    project = api.project.create(workspace_id, "converted data", change_name_if_conflict=True)
    project_id = project.id

dataset_id = sly.env.dataset_id(raise_not_found=False)
if dataset_id is None:
    dataset = api.dataset.create(project_id, "converted data ds", change_name_if_conflict=True)
    dataset_id = dataset.id

src_dir = "data"


# * 3. initialize importer and get converter
importer = ImportManager(src_dir)
converter = importer.converter

meta = converter.get_meta()
if project_id is not None:
    project = api.project.get_info_by_id(project_id)
    meta_json = api.project.get_meta(project_id)
    project_meta = sly.ProjectMeta.from_json(meta_json)

meta = project_meta.merge(meta)
api.project.update_meta(project_id, meta.to_json())


item_names = []
item_paths = []
anns = []
for item in converter.items:
    ann = converter.to_supervisely(item, meta)
    item_names.append(item.name)
    item_paths.append(item.path)
    anns.append(ann)
    # if len(anns) > 50:

img_infos = api.image.upload_paths(dataset_id, item_names, item_paths)
img_ids = [img_info.id for img_info in img_infos]
api.annotation.upload_anns(img_ids, anns)
anns = []
