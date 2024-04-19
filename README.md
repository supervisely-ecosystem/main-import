<div align="center" markdown>

<img align="center" src="https://github.com/supervisely-ecosystem/main-import/assets/79905215/8bbe4ed4-ad61-4ed1-af9a-c000f57e6593" width="250">

# Auto Import

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/main-import)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/main-import)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/main-import.png)](https://supervise.ly)

</div>

## Overview

The Auto Import is an all-in-one tool for importing data into Supervisely from a variety of sources. Whether you're an experienced user or just getting started, Import Wizard streamlines the import process, guiding you through each step to ensure smooth data import without the hassle.

The application supports various modalities and formats, it will automatically detect annotation format, verify, and import your data. When uploading to an existing project, the application will automatically validate and merge classes, tags, and annotations. If no format is detected, the application will import only items without annotations.

ℹ️ It is recommended to import samples of the data first to ensure that your data is compatible with the application.

ℹ️ To get started press the `Import Data` in your workspace/project/dataset and follow the instructions.

## Application key features:

1.  <b style="font-weight: 600; flex: none;" class="mr5">Image datasets:</b>

    - Auto-detect annotations in
      <span>
      <a href="https://github.com/supervisely-ecosystem/import-wizard-docs/blob/master/converter_docs/images/supervisely.md">Supervisely</a><span> | </span>
      <a href="https://github.com/supervisely-ecosystem/import-wizard-docs/blob/master/converter_docs/images/coco.md">COCO</a><span> | </span>
      <a href="https://github.com/supervisely-ecosystem/import-wizard-docs/blob/master/converter_docs/images/yolo.md">YOLO</a><span> | </span>
      <a href="https://github.com/supervisely-ecosystem/import-wizard-docs/blob/master/converter_docs/images/pascal.md">Pascal VOC</a><span> | </span>
      <a href="https://github.com/supervisely-ecosystem/import-wizard-docs/blob/master/converter_docs/images/cityscapes.md">Cityscapes</a><span> | </span>
      <a href="https://github.com/supervisely-ecosystem/import-wizard-docs/blob/master/converter_docs/images/masks.md">Images with PNG masks</a></span> formats.
    - Import images for
      <span>
      <a href="https://github.com/supervisely-ecosystem/import-wizard-docs/blob/master/converter_docs/images/multiview.md">Multi-view</a><span> | </span>
      <a href="https://github.com/supervisely-ecosystem/import-wizard-docs/blob/master/converter_docs/images/multispectral.md">Multispectral</a><span> | </span>
      <a href="https://github.com/supervisely-ecosystem/import-wizard-docs/blob/master/converter_docs/images/medical_2d.md">Medical 2D (single)</a>
      </span> labeling
    - Upload images as <a href="https://github.com/supervisely-ecosystem/import-wizard-docs/blob/master/converter_docs/images/csv.md">Links from CSV or TXT files</a> or convert <a href="https://github.com/supervisely-ecosystem/import-wizard-docs/blob/master/converter_docs/images/pdf.md">PDF pages to images</a>.
    - Images in any directory structure without annotations.

2.  <b style="font-weight: 600; flex: none;" class="mr5">Video datasets:</b>

    - Auto-detect annotations in
      <span>
      <a href="https://github.com/supervisely-ecosystem/import-wizard-docs/blob/master/converter_docs/videos/supervisely.md">Supervisely</a><span> | </span>
      DAVIS (coming soon) <span> | </span> MOT (coming soon) formats.
      </span>
    - Videos in any directory structure without annotations.

3.  <b style="font-weight: 600; flex: none;" class="mr5">Point clouds datasets:</b>

    - Auto-detect annotations in
      <span>
      <a href="https://github.com/supervisely-ecosystem/import-wizard-docs/blob/master/converter_docs/point_cloud/supervisely.md">Supervisely</a></span> format.
    - Point clouds in any directory structure without annotations in `PCD`, `LAS`, `LAZ`, `PLY` formats.

4.  <b style="font-weight: 600; flex: none;" class="mr5">Point clouds episodes datasets:</b>

    - Auto-detect annotations in
      <span>
      <a href="https://github.com/supervisely-ecosystem/import-wizard-docs/blob/master/converter_docs/point_cloud_episodes/supervisely.md">Supervisely</a></span> format.
    - Point cloud episodes without annotations in `PCD` format.

5.  <b style="font-weight: 600; flex: none;" class="mr5">Volumes datasets:</b>

    - Auto-detect annotations in
      <span>
      <a href="https://github.com/supervisely-ecosystem/import-wizard-docs/blob/master/converter_docs/volumes/supervisely.md">Supervisely</a></span> format.
    - Volumes in any directory structure without annotations in `DICOM`, `NRRD` formats.

6.  The application supports various sources: <span>Drag & Drop</span> | <span>Team Files</span> | <span>Agent Storage</span> | <span>Cloud Storage.</span>

7.  It will automatically detect the format of the files and import them.
8.  If no format is detected, the application will import only items without annotations.
9.  You can import data into a new or existing project or dataset.
10. You can specify only 1 format for the import.

## Need Help?

If you encounter any issues or have questions regarding Auto Import, don't hesitate to reach out to our support team in [Slack](https://supervisely.com/slack/).
