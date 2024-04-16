<div align="center" markdown>

<img align="center" src="https://github.com/supervisely-ecosystem/main-import/assets/79905215/8bbe4ed4-ad61-4ed1-af9a-c000f57e6593" width="250">

# Auto Import

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/main-import)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/main-import)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/main-import.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/main-import.png)](https://supervise.ly)

</div>

## Overview

The Auto Import is an all-in-one tool for importing data into Supervisely from a variety of sources. Whether you're an experienced user or just getting started, Import Wizard streamlines the import process, guiding you through each step to ensure smooth data import without the hassle.

The application supports various modalities and formats, it will automatically detect annotation format, verify, and import your data. When uploading to an existing project, the application will automatically validate and merge classes, tags, and annotations. If no format is detected, the application will import only items without annotations.

ℹ It is recommended to import samples of the data first to ensure that your data is compatible with the application.

## Application key features:

1.  It supports various modalities and formats:
    - images datasets in Supervisely, COCO, YOLO, Pascal, or Cityscapes formats or annotations from PNG masks.
    - images for multi-view, multispectral or medical data labeling.
    - images uploaded as links (just drop CSV file with available links to images).
    - images converted from PDF files or only images in any directory (without annotations).
    - videos datasets in Supervisely format (with annotations) or only videos in any directory (without annotations).
    - point clouds datasets in Supervisely format (with annotations) or only pointclouds in any directory in PCD, LAS, LAZ, PLY formats (without annotations)
    - volumes datasets in Supervisely format (with annotations) or only volumes in any directory in DICOM, NRRD formats (without annotations)
2.  It supports various sources:
    - Drag & Drop
    - Team Files
    - Agent Storage
    - Cloud Storage such as (S3, Google, or Azure) - available only in the Enterprise Edition ✨
3.  The application will automatically detect the format of the files and import them.
4.  If no format is detected, the application will import only items without annotations.
5.  You can import data into a new or existing project or dataset.
6.  You can specify only 1 format for the import.

## Need Help?

If you encounter any issues or have questions regarding Import Wizard, don't hesitate to reach out to our support team in [Slack](https://supervisely.com/slack/).
