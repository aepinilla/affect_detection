library(lme4)
library(tidyverse)

setwd("~/Documents/MATLAB/affect_detection/features/deap_offline")

# Create list of files
files_list <- list.files()

# Concatenate all files
all_files <- list()
for (file in 1:length(files_list)) {
  file_data <- read.csv(files_list[file])
  all_files <- bind_rows(all_files, file_data)
}

# Define power bands
bands <- list('delta', 'theta', 'alpha', 'beta', 'gamma')

#################### Valence #######################
# Define linear mixed models function
valence_results <- list()
for (b in bands) {
  # Subset data from current power band
  band_data <- all_files %>%
    filter(band == b)
  
  # Build full model
  valence.model = lmer(frontal_asymmetry ~ valence_rating + arousal_rating +
                         (1+valence_rating|participant) +
                         (1+valence_rating|video_id) +
                         (1+valence_rating|second),
                       data=band_data,
                       REML=FALSE,
                       control = lmerControl(calc.derivs = FALSE))
  
  # Build reduced model without valence ratings
  valence.null = lmer(frontal_asymmetry ~ arousal_rating +
                        (1+valence_rating|participant) +
                        (1+valence_rating|video_id) +
                        (1+valence_rating|second),
                      data=band_data,
                      REML=FALSE,
                      control = lmerControl(calc.derivs = FALSE))
  
  # Obtain likelihood ratio for valence dimension
  result_valence <- anova(valence.null,valence.model)
  valence_results[[sprintf('%s_valence', b)]] <- result_valence
}

print(valence_results)

#################### Arousal #######################
# Define linear mixed models function
arousal_results <- list()
for (b in bands) {
  # Subset data from current power band
  band_data <- all_files %>%
    filter(band == b)
  
  # Build full model
  arousal.model = lmer(frontal_asymmetry ~ arousal_rating + valence_rating +
                         (1+arousal_rating|participant) +
                         (1+arousal_rating|video_id) +
                         (1+arousal_rating|second),
                       data=band_data,
                       REML=FALSE,
                       control = lmerControl(calc.derivs = FALSE))
  
  # Build reduced model without valence ratings
  arousal.null = lmer(frontal_asymmetry ~ valence_rating +
                        (1+arousal_rating|participant) +
                        (1+arousal_rating|video_id) +
                        (1+arousal_rating|second),
                      data=band_data,
                      REML=FALSE,
                      control = lmerControl(calc.derivs = FALSE))
  
  # Obtain likelihood ratio for valence dimension
  result_arousal <- anova(arousal.model,arousal.null)
  arousal_results[[sprintf('%s_arousal', b)]] <- result_arousal
}

print(arousal_results)
