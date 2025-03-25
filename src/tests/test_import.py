import os

from dotenv import load_dotenv

import supervisely as sly
from supervisely.project.project_settings import LabelingInterface

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/demo_supervisely.env"))

sly.json.load_json_file
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


api = sly.Api()

team_id = sly.env.team_id()  # test data in team ID:447
workspace_id = sly.env.workspace_id()

# agent_id = 452
# module_id = 707
# module_info = api.app.get_ecosystem_module_info(module_id)

test_dirs_paths = {
    # "local": "/Users/almaz/job/supervisely/projects/main-import/test_files",
    "team_files": "/test_autoimport/",
    # "s3": "s3://remote-img-test/TESTS-NEW-IMPORT/",
    # "azure": "azure://supervisely-test/TEST-NEW-IMPORT/",
    # "google": "google://sly-dev-test/TEST-NEW-IMPORT/",
}

res_success, res_failed = [], []

import logging
sly.logger.setLevel(logging.ERROR)
# # UPLOAD ALL TEST FOLDERS
for source, test_dir in test_dirs_paths.items():
    print(f"{bcolors.HEADER}Source: {source}{bcolors.ENDC}")
    if sly.fs.dir_exists(test_dir):
        test_dirs = [
            os.path.join(test_dir, d)
            for d in os.listdir(test_dir)
            if os.path.isdir(os.path.join(test_dir, d))
        ]
        test_dirs = sorted(test_dirs)
    elif api.storage.dir_exists(team_id, test_dir):
        test_dirs = [
            info.path
            for info in api.storage.list(team_id, test_dir, recursive=False)
            if info.is_dir
        ]
    else:
        exit(0)

    for project_type in sly.ProjectType:
        print(f"{bcolors.OKCYAN}Project type: {project_type}{bcolors.ENDC}")
        project_name = f"{source}_{str(project_type)}"
        project = api.project.create(
            workspace_id,
            project_name,
            change_name_if_conflict=True,
            type=project_type,
        )
        # if project_type == sly.ProjectType.IMAGES:
        #     multi_view_project = api.project.create(
        #         workspace_id,
        #         project_name + "_multi_view",
        #         change_name_if_conflict=True,
        #         type=project_type,
        #     )
        #     multispectral_project = api.project.create(
        #         workspace_id,
        #         project_name + "_multispectral",
        #         change_name_if_conflict=True,
        #         type=project_type,
        #     )
        #     medical2d_project = api.project.create(
        #         workspace_id,
        #         project_name + "_medical2d",
        #         change_name_if_conflict=True,
        #         type=project_type,
        #     )
        #     matting_project = api.project.create(
        #         workspace_id,
        #         project_name + "_matting",
        #         change_name_if_conflict=True,
        #         type=project_type,
        #     )
        upload_as_links = False
        # if source in ["local", "team_files"] and upload_as_links:
        #     continue  # upload as links applicable only for cloud storages
        if sly.fs.dir_exists("/Users/almaz/job/supervisely/projects/main-import/temp"):
            sly.fs.clean_dir("/Users/almaz/job/supervisely/projects/main-import/temp")
        # sly.logger.info(f"Upload as links: {upload_as_links}")
        print(f"{bcolors.OKBLUE}Upload as links: {upload_as_links}{bcolors.ENDC}")
        for path in test_dirs:
            dir_name = os.path.basename(os.path.normpath(path))
            if str(project_type) in dir_name:
                labeling_interface = LabelingInterface.DEFAULT
                curr_project = project
                if "multi-view" in path:
                    continue
                    labeling_interface = LabelingInterface.MULTIVIEW
                    curr_project = multi_view_project
                elif "multispectral" in path:
                    continue
                    labeling_interface = LabelingInterface.MULTISPECTRAL
                    curr_project = multispectral_project
                elif "medical2d" in path:
                    continue
                    labeling_interface = LabelingInterface.MEDICAL_IMAGING_SINGLE
                    curr_project = medical2d_project
                elif "matting" in path:
                    continue
                    labeling_interface = LabelingInterface.IMAGE_MATTING
                    curr_project = matting_project

                if "links" in path:
                    continue
                    upload_as_links = True

                dataset_name = os.path.basename(path.rstrip("/"))
                dataset = api.dataset.create(
                    curr_project.id, dataset_name, change_name_if_conflict=True
                )
                try:

                    importer = sly.ImportManager(
                        path,
                        project_type,
                        labeling_interface=labeling_interface,
                        upload_as_links=upload_as_links,
                    )
                    importer.upload_dataset(dataset.id)

                    print(f"{bcolors.OKGREEN}Uploaded: {path}{bcolors.ENDC}")
                    res_success.append(path)
                except Exception as e:
                    print(f"{bcolors.FAIL}Failed: {path}{bcolors.ENDC}")
                    print(e)
                    res_failed.append(path)

print(f"{bcolors.OKCYAN}==============================={bcolors.ENDC}")
print(f"{bcolors.HEADER} Finished!{bcolors.ENDC}")
print(f"{bcolors.OKGREEN}Success: {len(res_success)}{bcolors.ENDC}")
print(f"{bcolors.FAIL}Failed: {len(res_failed)}{bcolors.ENDC}")
print(f"{bcolors.OKCYAN}==============================={bcolors.ENDC}")
# remote_path = None
# if project_type == sly.ProjectType.IMAGES:
#     remote_path = "s3://remote-img-test/TESTS-NEW-IMPORT/01. images SLY (from export)/"
# elif project_type == sly.ProjectType.VIDEOS:
#     remote_path = "s3://remote-img-test/TESTS-NEW-IMPORT/09. videos SLY (from export)/"
# if remote_path is not None:
#     dataset_name = os.path.basename(remote_path.rstrip("/"))
#     dataset = api.dataset.create(project.id, dataset_name, change_name_if_conflict=True)
#     importer = sly.ImportManager(remote_path, project_type, upload_as_links=True)
#     importer.upload_dataset(dataset.id)

# if project_type == sly.ProjectType.IMAGES:
#     params = module_info.get_arguments(
#         files_folder=path, images_project=project.id, images_dataset=dataset.id
#     )
# elif project_type == sly.ProjectType.VIDEOS:
#     params = module_info.get_arguments(
#         files_folder=path, videos_project=project.id, videos_dataset=dataset.id
#     )
# elif project_type == sly.ProjectType.POINT_CLOUDS:
#     params = module_info.get_arguments(
#         files_folder=path,
#         point_cloud_project=project.id,
#         point_cloud_dataset=dataset.id,
#     )
# elif project_type == sly.ProjectType.VOLUMES:
#     params = module_info.get_arguments(
#         files_folder=path, volumes_project=project.id, volumes_dataset=dataset.id
#     )
# elif project_type == sly.ProjectType.POINT_CLOUD_EPISODES:
#     params = module_info.get_arguments(
#         files_folder=path,
#         point_cloud_episodes_project=project.id,
#         point_cloud_episodes_dataset=dataset.id,
#     )
# else:
#     continue
# session = api.app.start(
#     agent_id=agent_id,
#     module_id=module_id,
#     workspace_id=workspace_id,
#     task_name=f"{source}",
#     params=params,
# )
# try:
#     api.app.wait(
#         session.task_id,
#         target_status=api.task.Status.FINISHED,
#         attempts=25,
#         attempt_delay_sec=5,
#     )

# except sly.WaitingTimeExceeded as e:
#     print(e)
#     api.app.stop(session.task_id)
# except sly.TaskFinishedWithError as e:
#     print(e)
# print("Task status: ", api.app.get_status(session.task_id))

# # UPLOAD SINGLE FOLDER
# project_id = sly.env.project_id(raise_not_found=False)
# dataset_id = sly.env.dataset_id(raise_not_found=False)
# project_modality = sly.ProjectType.IMAGES  # sly.env.project_modality()
# src_dir = "images"
# start_import(src_dir, "new converted data", project_modality)

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
