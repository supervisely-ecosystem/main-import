from __future__ import annotations

import datetime
import os
from dataclasses import dataclass
from typing import List, Optional, Union

import supervisely as sly
from supervisely.convert.volume.nii.nii_planes_volume_converter import (
    NiiPlaneStructuredAnnotationConverter,
)

from src import functions as f


InputPaths = Union[str, List[str]]


@dataclass
class ImportContext:
    project: sly.ProjectInfo
    dataset: Optional[sly.DatasetInfo]
    dataset_id: int
    dataset_name: str
    labeling_interface: str
    project_modality: str
    dataset_created: bool = False
    project_created: bool = False


@dataclass
class ImportResult:
    project: sly.ProjectInfo
    dataset: Optional[sly.DatasetInfo]
    dataset_id: int
    output_title: str
    project_created: bool
    dataset_created: bool


def _default_dataset_name() -> str:
    return f"dataset {datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}"


def resolve_dataset_name(api: sly.Api, project_id: int, dataset_name: Optional[str]) -> str:
    if dataset_name is None or dataset_name == "":
        dataset_name = _default_dataset_name()
    existing_ds_names = set(ds.name for ds in api.dataset.get_list(project_id, recursive=True))
    return sly.generate_free_name(existing_ds_names, dataset_name, False, True)


def prepare_import(
    api: sly.Api,
    project_id: int,
    dataset_id: Optional[int],
    dataset_name: Optional[str],
) -> ImportContext:
    project = api.project.get_info_by_id(project_id)
    if project is None:
        raise Exception(f"Project with id={project_id} not found")
    os.environ.setdefault("TEAM_ID", str(project.team_id))
    os.environ.setdefault("WORKSPACE_ID", str(project.workspace_id))

    labeling_interface = f.get_labeling_interface(api, project)
    dataset = None
    dataset_created = False
    if dataset_id:
        dataset = api.dataset.get_info_by_id(dataset_id)
    if dataset is None:
        dataset_name = resolve_dataset_name(api, project.id, dataset_name)
        dataset = api.dataset.create(project.id, dataset_name, change_name_if_conflict=True)
        dataset_created = True
    else:
        dataset_name = dataset.name

    return ImportContext(
        project=project,
        dataset=dataset,
        dataset_id=dataset.id,
        dataset_name=dataset_name,
        labeling_interface=labeling_interface,
        project_modality=project.type,
        dataset_created=dataset_created,
    )


def detect_importer(
    input_paths: Optional[InputPaths],
    project_modality: str,
    labeling_interface: str,
    import_as_links: bool,
) -> sly.ImportManager:
    if input_paths is None:
        raise Exception("Please, provide data to import.")
    return sly.ImportManager(
        input_paths,
        project_modality,
        labeling_interface=labeling_interface,
        upload_as_links=import_as_links,
    )


def upload_import(importer: sly.ImportManager, dataset_id: int) -> Optional[int]:
    return importer.upload_dataset(dataset_id)


def finalize_import(
    api: sly.Api,
    context: ImportContext,
    importer: sly.ImportManager,
    new_dataset_id: Optional[int],
) -> ImportResult:
    project = context.project
    dataset = context.dataset
    dataset_id = context.dataset_id
    project_created = context.project_created

    if new_dataset_id is not None:
        project_created = True

    if hasattr(importer.converter, "blob_project") and importer.converter.blob_project:
        sly.logger.info(
            "Data was uploaded in blob format. "
            "All items have been added to the top level of the project. "
        )
        if context.dataset_created:
            sly.logger.info("Cleaning up unused dataset...")
            api.dataset.remove(dataset_id)
            sly.logger.info(f"Dataset '{dataset.name}' was removed. ")
        output_title = f"{project.name}"
    else:
        prefix_parts = []
        if context.dataset_created:
            prefix_parts.append("New ")
        if project_created:
            dataset_id = new_dataset_id
            dataset = api.dataset.get_info_by_id(dataset_id)
            project = api.project.get_info_by_id(dataset.project_id)
            sly.logger.info("New project and dataset were created during import process.")
            sly.logger.info(f"Project: '{project.name}' (ID: {project.id})")
            sly.logger.info(f"Dataset: '{dataset.name}' (ID: {dataset.id})")
        if "dataset" not in dataset.name.lower():
            prefix_parts.append("Dataset: ")

        prefix = "".join(prefix_parts)
        output_title = f"{project.name}. {prefix}{dataset.name}".strip()

    if isinstance(importer.converter, NiiPlaneStructuredAnnotationConverter):
        if context.dataset_created:
            sly.logger.info("Cleaning up unused dataset...")
            api.dataset.remove(dataset_id)
            sly.logger.info(f"Dataset '{dataset.name}' was removed. ")

    return ImportResult(
        project=project,
        dataset=dataset,
        dataset_id=dataset_id,
        output_title=output_title,
        project_created=project_created,
        dataset_created=context.dataset_created,
    )


def run_import(
    api: sly.Api,
    input_paths: Optional[InputPaths],
    project_id: int,
    dataset_id: Optional[int] = None,
    dataset_name: Optional[str] = None,
    import_as_links: bool = False,
) -> ImportResult:
    context = prepare_import(api, project_id, dataset_id, dataset_name)
    importer = detect_importer(
        input_paths,
        context.project_modality,
        context.labeling_interface,
        import_as_links,
    )
    new_dataset_id = upload_import(importer, context.dataset_id)
    return finalize_import(api, context, importer, new_dataset_id)
