# Interlinear glossing with CRF

## CRF glossing pipeline demonstration
A demonstration notebook of the pipeline is available in the `demonstration` folder.
The whole pipeline is used step by step to generate glosses for the Gitksan sentences from the [SIGMORPHON 2023 Shared Task on Interlinear Glossing](https://github.com/sigmorphon/2023GlossingST).

The input IGT data should look as follows:
```
\t Ap yukwhl ha'niisgwaa'ytxw.
\m ap yukw-hl ha-'nii-sgwaa'ytxw
\g VER IPFV-CN INS-on-rest
\l But it was Sunday.
```
- `\t` indicates the source sentence 
- `\m` is the same sentence segmented into morphemes
- `\g` represents the interlinear gloss (necessary in the training dataset)
- `\l` shows the translation in the target (or documentation) language.

The pipeline only relies on CRFsuite (more exactly, `sklearn_crfsuite`, see [here](https://sklearn-crfsuite.readthedocs.io)).

## Conversion scripts for ELAN and Toolbox
This repository also includes conversion scripts to support more data formats for interlinear glossing (in the `format_conversion` folder).

- `elan_to_pipeline.py`: Converts ELAN exports to a format compatible with the CRF pipeline.
- `pipeline_to_elan.py`: Converts CRF results back into ELAN-readable format.
- `toolbox_to_pipeline.py`: Converts Toolbox-formatted IGT data to the CRF pipeline format.

These scripts aim to facilitate the data format conversion when using the glossing pipeline with existing linguistic annotation tools.

## Citation
