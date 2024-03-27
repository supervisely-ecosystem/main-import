import os

from dotenv import load_dotenv

import supervisely as sly
from supervisely.api.file_api import FileInfo

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()
team_id = sly.env.team_id()

# * Set up test paths for different storages
folders = [
    "/tmp/test_img/",
    "s3://remote-img-test/test_img-2/",
    "azure://supervisely-test/test_img/",
    "google://sly-dev-test/test_img/",
    # # without trailing slash
    # "/tmp/test_img",
    # "s3://remote-img-test/test_img-2",
    # "azure://supervisely-test/test_img",
    # "google://sly-dev-test/test_img",
]
agent_path = "agent://359/app_data/import-dataset/53924/2024-02-27 22:10:10.725/06. images YOLO bboxes (from export)/"


not_none_fields_cnt = None
not_none_folder_fields_cnt = None
for path in folders:
    sly.fs.clean_dir("temp")
    dir_exists = api.storage.dir_exists(team_id, path)
    assert dir_exists, f"Directory should exist: {path}"

    file_exists = api.storage.exists(team_id, path)
    assert not file_exists, f"It should be a directory: {path}"

    dir_exists = api.storage.dir_exists(team_id, path + "_not_exist")
    assert not dir_exists, f"Directory should not exist: {path}_not_exist"

    dir_info = api.storage.list(team_id, path)
    assert len(dir_info) == 8, f"Should be a list of 8 file infos: {path}"

    first_item = dir_info[0]
    assert type(first_item) == FileInfo, f"Should be a list of file infos: {path}"

    file_exists = api.storage.exists(team_id, first_item.path)
    assert file_exists, f"File should exist: {path}"

    dir_exists = api.storage.dir_exists(team_id, first_item.path)
    assert not dir_exists, f"It should be a file: {path}"

    file_exists = api.storage.exists(team_id, first_item.path + "_not_exist")
    assert not file_exists, f"File should not exist: {path}_not_exist"

    not_none_fields = [
        field for field in first_item._asdict().keys() if getattr(first_item, field) is not None
    ]
    if path not in ["/tmp/test_img/", "/tmp/test_img"]:
        if not_none_fields_cnt is None:
            not_none_fields_cnt = len(not_none_fields)
        else:
            assert not_none_fields_cnt == len(
                not_none_fields
            ), f"Should be the same number of not None fields: {path}"

    dir_info = api.storage.list(team_id, path, recursive=False)
    assert len(dir_info) == 3, f"Should be a list of 3 file/folder infos: {path}"

    dir_info = api.storage.list(team_id, path, limit=2)
    assert len(dir_info) == 2, f"Should be a list of 2 file/folder infos: {path}"

    dir_info = api.storage.list(team_id, path, recursive=False, limit=2)
    assert len(dir_info) == 2, f"Should be a list of 2 file/folder infos: {path}"

    dir_info = api.storage.list(team_id, path, return_type="dict")
    assert len(dir_info) == 8, f"Should be a list of 8 files: {path}"
    assert type(dir_info[0]) == dict, "Should be a list of dicts: /tmp/test img/"

    dir_info = api.storage.list(team_id, path, recursive=False, return_type="dict")
    assert len(dir_info) == 3, f"Should be a list of 3 file infos: {path}"
    assert type(dir_info[0]) == dict, "Should be a list of dicts: /tmp/test img/"

    if path not in ["/tmp/test_img/", "/tmp/test_img"]:
        folder_items = [item for item in dir_info if item["type"] == "folder"]
        if len(folder_items) > 0:
            first_folder_item = folder_items[0]
            not_none_folder_fields = [
                field for field in first_folder_item.keys() if first_folder_item[field] is not None
            ]
            if not_none_folder_fields_cnt is None:
                not_none_folder_fields_cnt = len(not_none_folder_fields)
            else:
                assert not_none_folder_fields_cnt == len(
                    not_none_folder_fields
                ), f"Should be the same number of not None fields: {path}"

    local_path = os.path.join("temp", os.path.basename(path.rstrip("/")))
    api.storage.download_directory(team_id, path, local_path)
    assert os.path.exists(local_path), f"Directory should be downloaded: {path}"
    assert (
        sum(d.stat().st_size for d in os.scandir(".") if d.is_file()) > 0
    ), f"Directory should have size > 0: {path}"

    local_file_path = os.path.join("temp", first_item.name)
    api.storage.download(team_id, first_item.path, local_file_path)
    assert os.path.exists(local_file_path), f"File should be downloaded: {path}"
    assert os.path.getsize(local_file_path) > 0, f"File should have size > 0: {path}"

    new_remote_path = path.rstrip("/") + "_new"
    new_remote_path = api.storage.upload_directory(team_id, local_path, new_remote_path)
    assert api.storage.dir_exists(team_id, new_remote_path), f"Directory should be uploaded: {path}"

    new_remote_file_path = new_remote_path + "/" + f"new_{first_item.name}"
    file_info = api.storage.upload(team_id, local_file_path, new_remote_file_path)
    new_remote_file_path = file_info.path
    assert api.storage.exists(team_id, new_remote_file_path), f"File should be uploaded: {path}"

    api.storage.remove(team_id, new_remote_file_path)
    assert not api.storage.exists(team_id, new_remote_file_path), f"File should be removed: {path}"

    api.storage.upload(team_id, local_file_path, new_remote_file_path)
    api.storage.remove_file(team_id, new_remote_file_path)
    assert not api.storage.exists(team_id, new_remote_file_path), f"File should be removed: {path}"

    api.storage.remove_dir(team_id, new_remote_path)
    assert not api.storage.dir_exists(team_id, new_remote_path), f"Directory not removed: {path}"

    dir_size = api.storage.get_directory_size(team_id, path)
    assert dir_size > 0, f"Directory should have size: {path}"

    file_info = api.storage.get_info_by_path(team_id, first_item.path)
    assert file_info is not None, f"File info should be returned: {path}"

    sly.fs.clean_dir("temp")

# for agent path
dir_info = api.storage.list(team_id, agent_path)
assert len(dir_info) == 5, f"Should be a list of 8 file infos: {agent_path}"

first_item = dir_info[0]
assert type(first_item) == FileInfo, f"Should be a list of file infos: {agent_path}"

dir_info = api.storage.list(team_id, agent_path, recursive=False)
assert len(dir_info) == 3, f"Should be a list of 3 file/folder infos: {agent_path}"

dir_info = api.storage.list(team_id, agent_path, limit=2)
assert len(dir_info) == 2, f"Should be a list of 2 file/folder infos: {agent_path}"

dir_info = api.storage.list(team_id, agent_path, recursive=False, limit=2)
assert len(dir_info) == 2, f"Should be a list of 2 file/folder infos: {agent_path}"

dir_info = api.storage.list(team_id, agent_path, return_type="dict")
assert len(dir_info) == 5, f"Should be a list of 8 files: {agent_path}"
assert type(dir_info[0]) == dict, "Should be a list of dicts: /tmp/test img/"

dir_info = api.storage.list(team_id, agent_path, recursive=False, return_type="dict")
assert len(dir_info) == 3, f"Should be a list of 3 file infos: {agent_path}"
assert type(dir_info[0]) == dict, "Should be a list of dicts: /tmp/test img/"

dir_exists = api.storage.dir_exists(team_id, agent_path)
assert dir_exists, f"Directory should exist: {agent_path}"

dir_exists = api.storage.dir_exists(team_id, agent_path + "not_exist")
assert not dir_exists, f"Directory should not exist: {agent_path}"

print("\033[92mStorage API tests passed\033[0m")
