import os

from dotenv import load_dotenv

import supervisely as sly
from supervisely.convert.converter import ImportManager

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))


api = sly.Api()


src_dir = "data"

# * 3. initialize importer and get converter
importer = ImportManager(src_dir)
converter = importer.converter  # -> sly.ImageFormatConverter

meta = converter.get_meta()  # -> sly.ProjectMeta
# classes = converter.get_classes()  # sly.ObjClassCollection
# tags = converter.get_tags()  # sly.TagMetaCollection
# ds_meta = sly.ProjectMeta(obj_classes=classes, tag_metas=tags)
# project_meta = project_meta.merge(ds_meta)  # ? could be conflicts

# * 5. List items (return image-ann mapping)
items = converter.get_items(resolve_conflicts=True)  # ! generator
# {"item_name.jpg": {"item": "path/to/item_name.jpg", "ann": "path/to/item_name.jpg.json"}, ...}
# # or
# items = converter.get_items()
# anns = converter.get_anns()


meta = converter.get_meta()
items = converter.get_items()

item_names = []
item_paths = []
anns = []
for item_path, ann_path in converter:
    ann = converter.to_supervisely(item_path, ann_path, meta)
    anns.append(ann)
    if len(anns) > 50:
        img_infos = api.image.upload_paths(dataset.id, item_names, item_paths)
        img_ids = [img_info.id for img_info in img_infos]
        api.annotation.upload_anns(img_ids, anns)
        anns = []
