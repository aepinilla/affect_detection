# Affect detection

## Instructions
1. Install R (https://cran.r-project.org/)
2. Clone this repository:
```
git clone git@github.com:aepinilla/affect_detection.git
```
2. Download the 'data.zip' file from the OSF repository of the study: https://osf.io/7v9kt/
3. Unzip data.zip and place it at the root of the folder you just cloned.
6. Using the terminal, go to the root of the 'affect_detection' folder and run:
```
python main.py
```

## Preprocessing
The 'data' folder contains data that has been already preprocessed. To replicate the preprocessing steps, follow these instructions:
1. Install Matlab.
2. Install EEGLAB following these instructions: https://eeglab.org/tutorials/01_Install/Install.html
4. Transform XDF files to CSV for faster processing:
```
python xdf_to_csv.py
```
6. Open EEGLAB in Matlab and run the preprocessing script located at affect_detection/src/preprocessing.m

## Reports
All files generated by main.py will be stored in the 'reports' folder. In a MacBook Pro, it took several hours to run the program. If you want to skip that, download the 'reports.zip' file available in the OSF repository: https://osf.io/7v9kt/