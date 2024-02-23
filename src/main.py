import os

from dotenv import load_dotenv

import supervisely as sly
from supervisely.convert.converter import ImportManager

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))


api = sly.Api()


project_id = sly.env.project_id()
dataset_id = sly.env.dataset_id(raise_not_found=False)
dataset_name = os.getenv("DATASET_NAME", None)


# * 1. Get project and dataset infos
project = api.project.get_info_by_id(project_id)
project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))

if dataset_id:
    dataset = api.dataset.get_info_by_id(dataset_id)
elif dataset_name:
    dataset = api.dataset.get_info_by_name(project_id, dataset_name)
else:
    raise RuntimeError("Dataset not specified.")


# * 2. Get input path and download data
src_dir = "data"
api.file.download_input(src_dir)
# check if files in src_dir are an archive and unpack them if so
# listdir = os.listdir(src_dir)
# if len(listdir) == 1:
#     file_path = os.path.join(src_dir, listdir[0])
#     if os.path.isfile(file_path) and sly.fs.is_archive(file_path):
#         sly.fs.unpack_archive(file_path, src_dir)
#         os.remove(file_path)
# or recursively...


# * 3. initialize importer and get converter
importer = ImportManager(src_dir)
converter = importer.get_converter()
# or
# converter = sly.Converter.get_converter(input_path)

# * 4. Get classes and tags info
meta = converter.get_meta()
# classes = converter.get_classes()  # ? sly.ObjClassCollection
# tags = converter.get_tags()  # ? sly.TagMetaCollection
# # ? or [{"name": "car", "geometry_type": "bitmap", "color": None}, ...]
# # ? or [{"name": "size", "value_type": "string", "value": "small"}, ...]
# # or
# ds_meta = sly.ProjectMeta(obj_classes=classes, tag_metas=tags)
# project_meta = project_meta.merge(ds_meta) # ? could be conflicts

# * 5. List items (return image-ann mapping)
items = converter.get_items(resolve_conflicts=True)  # ! generator
# {"item_name.jpg": {"item": "path/to/item_name.jpg", "ann": "path/to/item_name.jpg.json"}, ...}
# # or
# items = converter.get_items()
# anns = converter.get_anns()


# * 6. Preview sample
# ? previews = converter.preview(sample_size=5) # will be done inside the SDK
# or
previews = []
for i in range(5):
    item = items[i]
    image_path = item["image"]
    ann_path = item["ann"]

    ann: sly.Annotation = converter.to_supervisely(image_path, ann_path)  # , project_meta)
    img = sly.image.read(image_path)
    ann.draw_pretty(img)
    previews.append(img)


# * 7 Convert and upload

## * Option 1: convert all data to supervisely format locally and then upload dataset
sly_dataset = "path/to/supervisely"
converter.all_to_supervisely(sly_dataset)  # convert all data to supervisely format locally
api.dataset.upload(dataset.id, sly_dataset)  # ? need new SDK method for this

## * Option 2: simple upload data (all processing will be done inside the SDK)
importer.upload_dataset(dataset.id, sly_dataset)

## * Option 3: upload data in batches
meta = converter.get_meta()
items = converter.get_items()
anns = []
for item_path, ann_path in converter:
    ann = converter.to_supervisely(img_path, ann_path, meta)
    anns.append(ann)
    if len(anns) > 50:
        img_infos = api.image.upload_paths(dataset.id, item_names, img_paths)
        img_ids = [img_info.id for img_info in img_infos]
        api.annotation.upload_anns(img_ids, anns)
        anns = []


# TODO list:
# - [ ] self._annotations – check if it is necessary (or remove it)
# - [ ] global var MODALITY, optimize detect_modality
# - [ ] configure convenient module import (ex: import supervisely.convert.image.COCOFORMAT)
# - [ ] rename file converter.py? rename class ImportManager?
# - [ ] rename images (items) if exists in the dataset (while uploading)
