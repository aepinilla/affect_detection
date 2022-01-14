library(lme4)
library(tidyverse)

setwd("~/Documents/MATLAB/affect_detection/features/pilot_exp")

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

#################### Negativity #######################
# Define linear mixed models function
negativity_results <- list()
for (b in bands) {
  # Subset data from current power band
  band_data <- all_files %>%
    filter(band == b)
  
  # Build full model
  negativity.model = lmer(frontal_asymmetry ~ negativity_rating + positivity_rating + net_predisposition_rating +
                            (1+negativity_rating|participant) +
                            (1+negativity_rating|video_id) +
                            (1+negativity_rating|second),
                          data=band_data,
                          REML=FALSE,
                          control = lmerControl(calc.derivs = FALSE))
  
  # Build reduced model without valence ratings
  negativity.null = lmer(frontal_asymmetry ~ positivity_rating + net_predisposition_rating +
                           (1+negativity_rating|participant) +
                           (1+negativity_rating|video_id) +
                           (1+negativity_rating|second),
                         data=band_data,
                         REML=FALSE,
                         control = lmerControl(calc.derivs = FALSE))
  
  # Obtain likelihood ratio for negativity dimension
  result_negativity <- anova(negativity.null, negativity.model)
  negativity_results[[sprintf('%s_negativity', b)]] <- result_negativity
}

print(negativity_results)

#################### Positivity #######################
# Define linear mixed models function
positivity_results <- list()
for (b in bands) {
  # Subset data from current power band
  band_data <- all_files %>%
    filter(band == b)
  
  # Build full model
  positivity.model = lmer(frontal_asymmetry ~ negativity_rating + positivity_rating + net_predisposition_rating +
                            (1+positivity_rating|participant) +
                            (1+positivity_rating|video_id) +
                            (1+positivity_rating|second),
                          data=band_data,
                          REML=FALSE,
                          control = lmerControl(calc.derivs = FALSE))
  
  # Build reduced model without valence ratings
  positivity.null = lmer(frontal_asymmetry ~ negativity_rating + net_predisposition_rating +
                           (1+positivity_rating|participant) +
                           (1+positivity_rating|video_id) +
                           (1+positivity_rating|second),
                         data=band_data,
                         REML=FALSE,
                         control = lmerControl(calc.derivs = FALSE))
  
  # Obtain likelihood ratio for positivity dimension
  result_positivity <- anova(positivity.null,positivity.model)
  positivity_results[[sprintf('%s_positivity', b)]] <- result_positivity
}

print(positivity_results)


#################### Net Predisposition #######################
# Define linear mixed models function
net_predisposition_results <- list()
for (b in bands) {
  # Subset data from current power band
  band_data <- all_files %>%
    filter(band == b)
  
  # Build full model
  net_predisposition.model = lmer(frontal_asymmetry ~ negativity_rating + positivity_rating + net_predisposition_rating +
                                    (1+net_predisposition_rating|participant) +
                                    (1+net_predisposition_rating|video_id) +
                                    (1+net_predisposition_rating|second),
                                  data=band_data,
                                  REML=FALSE,
                                  control = lmerControl(calc.derivs = FALSE))
  
  # Build reduced model without valence ratings
  net_predisposition.null = lmer(frontal_asymmetry ~ negativity_rating + positivity_rating +
                                   (1+net_predisposition_rating|participant) +
                                   (1+net_predisposition_rating|video_id) +
                                   (1+net_predisposition_rating|second),
                                 data=band_data,
                                 REML=FALSE,
                                 control = lmerControl(calc.derivs = FALSE))
  
  # Obtain likelihood ratio for net_predisposition dimension
  result_net_predisposition <- anova(net_predisposition.null,net_predisposition.model)
  net_predisposition_results[[sprintf('%s_net_predisposition', b)]] <- result_net_predisposition
}

print(net_predisposition_results)
