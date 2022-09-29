# Affect detection

## Dataset
1. Download the 'data' folder from the OSF repository of the study: https://osf.io/5m3yu/
2. Place the 'data' folder inside the 'affect_detection' folder.

## Instructions
```
1. git@github.com:aepinilla/affect_detection.git
2. Go to src/feature_selection/lme_models
3. Open the 3 R files located in the 'lme_models' folder.
4. Edit the line 15 of each of those files, according to the path to your working directory/
5. From the root folder run: python main.py
```

## Preprocessing
The 'data' folder contains data that has been already preprocessed. To replicate the preprocessing steps, follow these steps:
1. Install Matlab.
2. Install EEGLAB following these instructions: https://eeglab.org/tutorials/01_Install/Install.html
3. Clone this repository to the MATLAB folder
4. Transform XDF files to CSV for faster processing:
```
python xdf_to_csv.py
```
6. Open EEGLAB in Matlab and run preprocessing script located in src/preprocessing.m

