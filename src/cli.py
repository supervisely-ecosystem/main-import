import argparse
import os
import sys
import traceback
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def _env_int(name: str) -> Optional[int]:
    value = os.environ.get(name)
    if value is None or value == "":
        return None
    return int(value)


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "y"}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Import local data to Supervisely.")
    parser.add_argument(
        "--input",
        default=os.environ.get("INPUT_PATH", "/input"),
        help="Path to input data inside the container. Defaults to /input.",
    )
    parser.add_argument(
        "--project-id",
        type=int,
        default=_env_int("PROJECT_ID"),
        required=os.environ.get("PROJECT_ID") in {None, ""},
        help="Destination Supervisely project ID.",
    )
    parser.add_argument(
        "--dataset-id",
        type=int,
        default=_env_int("DATASET_ID"),
        help="Optional destination dataset ID.",
    )
    parser.add_argument(
        "--dataset-name",
        default=os.environ.get("DATASET_NAME"),
        help="Optional dataset name when a new dataset is created.",
    )
    parser.add_argument(
        "--import-as-links",
        action="store_true",
        default=_env_bool("IMPORT_AS_LINKS"),
        help="Upload supported entities as links.",
    )
    parser.add_argument(
        "--work-dir",
        default=os.environ.get("SLY_APP_DATA_DIR", "/tmp/sly-import-work"),
        help="Temporary work directory inside the container.",
    )
    parser.add_argument(
        "--env-file",
        default=None,
        help="Optional dotenv file to load before connecting to Supervisely.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()

    if args.env_file:
        load_dotenv(Path(args.env_file).expanduser())

    os.environ["SLY_APP_DATA_DIR"] = args.work_dir

    import supervisely as sly
    from src.import_runner import run_import

    try:
        sly_version = version("supervisely")
    except PackageNotFoundError:
        sly_version = "unknown"
    sly.logger.info(f"Supervisely SDK version: {sly_version}")

    input_path = Path(args.input)
    if not input_path.exists():
        sly.logger.error(f"Input data not found: {input_path}")
        return 1

    app_data = sly.app.get_data_dir()
    sly.fs.clean_dir(app_data)

    try:
        api = sly.Api.from_env()
        result = run_import(
            api=api,
            input_paths=str(input_path),
            project_id=args.project_id,
            dataset_id=args.dataset_id,
            dataset_name=args.dataset_name,
            import_as_links=args.import_as_links,
        )
        sly.logger.info(
            f"Import finished. Project: '{result.project.name}' (ID: {result.project.id}). "
            f"Output: {result.output_title}"
        )
        return 0
    except Exception as exc:
        sly.logger.error(
            "Import failed. If the container runs out of disk space while staging or "
            "unpacking data, run it with a larger Docker temporary/work volume.",
            exc_info=True,
        )
        print(f"Import failed: {exc}", file=sys.stderr)
        traceback.print_exc()
        return 1
    finally:
        sly.fs.clean_dir(app_data)


if __name__ == "__main__":
    sys.exit(main())
