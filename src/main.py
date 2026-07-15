import src.functions as f
import src.globals as g
import src.import_runner as runner
import supervisely as sly

# * 1. Get project and dataset infos
try:
    context = runner.prepare_import(g.api, g.project_id, g.dataset_id, g.dataset_name)
    g.dataset_id = context.dataset_id
    g.project_modality = context.project_modality
except Exception as e:
    f.handle_exception_and_stop(e, "Error occurred. Please, contact support")


# * 2. initialize importer to detect format
try:
    importer = runner.detect_importer(
        g.input_paths,
        context.project_modality,
        context.labeling_interface,
        g.import_as_links,
    )
except Exception as e:
    f.handle_exception_and_stop(e, "Format was not recognized")

# * 3 Convert and upload data
try:
    new_dataset_id = runner.upload_import(importer, g.dataset_id)
except Exception as e:
    f.handle_exception_and_stop(e, "Failed to convert and upload data. Please, check the logs")

result = runner.finalize_import(g.api, context, importer, new_dataset_id)
g.dataset_id = result.dataset_id

# * 4. Set output project
g.api.task.set_output_project(g.task_id, result.project.id, result.output_title)
g.workflow.add_output(result.project)

# * 5. Clean app_data directory
sly.fs.clean_dir(g.app_data)
