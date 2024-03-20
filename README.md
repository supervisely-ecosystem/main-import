<div align="center" markdown>
<img src="https://github.com/supervisely-ecosystem/main-import/releases/download/v1.0.0/poster.png"/>

# Import Wizard

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#Format-Examples">Format Examples</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/main-import)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/main-import)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/main-import.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/main-import.png)](https://supervise.ly)

</div>

# Overview

The Import Wizard is an application that allows you to import datasets easily.

ℹ It is recommended to import samples of the data first to ensure that your data is compatible with the application.

**Application key features:**

1.  It supports various modalities and formats:
    - images datasets in Supervisely, COCO, YOLO, Pascal formats or only images.
    - videos datasets in Supervisely, MOT, DAVIS formats or only videos.
    - point clouds datasets in Supervisely, LAS, LAZ, PLY formats or only pointclouds.
    - volumes datasets in Supervisely, DICOM formats or only volumes.
2.  It supports various sources:
    - Drag&Drop
    - Team Files
    - Agent Storage
    - Cloud Storage such as AWS S3, Google Cloud Storage, or Azure Blob Storage. Available only in Enterprise Edition
    - File systems
3.  The application will automatically detect the format of the files and import them.
4.  If no format is detected, the application will import only items without annotations.
5.  You can import data into a new or existing project/dataset.
6.  You can specify only 1 format for the import. If you want to import multiple formats, you can run the application multiple times.

ℹ Import from Cloud Storage is available only in the Enterprise Edition.

# How to Run

**1. Specify destination**

You can specify the destination of the data in the following ways:

1.  Specify whether you want to create a new project or use an existing one
    - If you choose a new project, specify the modality and project name
    - You can also specify the classes/tags for the new project
2.  Specify destination dataset:
    - If you choose an existing project, you can select the dataset where you want to import the data (or create a new one)
    - If you are importing to a new dataset, specify the dataset name

**2. Choose the source of the data**
Choose the source of the data (D&D, from Team files, Agent storage, Cloud storage, or file systems) using the UI accordion widget.

**3. Select the desired data**
Drag and drop or select the data you want to import.

**4. Run the application**
Press the Run button to start the import process.

# Format examples

Here are examples of the supported formats.

Folder structure sensitive formats:

- Images:
  - [Pascal](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/index.html)
- Volumes:
  - [Supervisely](https://docs.supervise.ly/data-organization/00_ann_format_navi)

Folder structure insensitive formats:

- Images:
  - [Supervisely](https://docs.supervise.ly/data-organization/00_ann_format_navi)
  - [COCO](https://cocodataset.org/#format-data)
  - [YOLO]()
- Videos:
  - [Supervisely](https://docs.supervise.ly/data-organization/00_ann_format_navi)
  - [MOT](https://motchallenge.net/instructions/)
  - [DAVIS](https://davischallenge.org/davis2017/code.html)
- Point Clouds:
  - [Supervisely](https://docs.supervise.ly/data-organization/00_ann_format_navi)
  - [LAS](https://www.asprs.org/wp-content/uploads/2010/12/LAS_1_4_r13.pdf)
  - [LAZ](https://www.asprs.org/wp-content/uploads/2010/12/LAS_1_4_r13.pdf)
  - [PLY](http://paulbourke.net/dataformats/ply/)
- Volumes:
  - [DICOM](https://www.dicomstandard.org/current/)
