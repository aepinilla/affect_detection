library(lme4)
library(tidyverse)

setwd("~/Documents/MATLAB/affect_detection/features/deap_offline")

# Create list of files
files_list <- list.files()

# Concatenate all files
#all_files <- list()
#for (file in 1:length(files_list)) {
#  file_data <- read.csv(files_list[file])
#  all_files <- bind_rows(all_files, file_data)
#}

test_data_1 <- read.csv(files_list[1])
test_data_2 <- read.csv(files_list[2])
test_data <-  bind_rows(test_data_1, test_data_2)


# Define power bands
bands <- list('delta', 'theta', 'alpha', 'beta', 'gamma')

# Define linear mixed models function
#deap_lmm <- function(deap_data) {
# Create empty vector to store results from each power band

#bands_results <- vector()
#for (b in bands) {
# Subset data from current power band
band_data <- test_data %>%
  filter(band == 'alpha')

# Build full model
band.model = lmer(frontal_asymmetry ~ valence_rating + arousal_rating +
                    (1+valence_rating|participant) +
                    (1+valence_rating|video_id) +
                    (1+valence_rating|time_stamp) +
                    (1+arousal_rating|participant) +
                    (1+arousal_rating|video_id) +
                    (1+arousal_rating|time_stamp),
                  data=band_data,
                  REML=FALSE,
                  control = lmerControl(calc.derivs = FALSE))

# Build reduced model without valence ratings
band.null_valence = lmer(frontal_asymmetry ~ arousal_rating +
                           (1+valence_rating|participant) +
                           (1+valence_rating|video_id) +
                           (1+valence_rating|time_stamp) +
                           (1+arousal_rating|participant) +
                           (1+arousal_rating|video_id) +
                           (1+arousal_rating|time_stamp),
                         data=band_data,
                         REML=FALSE,
                         control = lmerControl(calc.derivs = FALSE))

# Build reduced model without arousal ratings
band.null_arousal = lmer(frontal_asymmetry ~ valence_rating +
                           (1+valence_rating|participant) +
                           (1+valence_rating|video_id) +
                           (1+valence_rating|time_stamp) +
                           (1+arousal_rating|participant) +
                           (1+arousal_rating|video_id) +
                           (1+arousal_rating|time_stamp),
                         data=band_data,
                         REML=FALSE,
                         control = lmerControl(calc.derivs = FALSE))

# Obtain likelihood ratio for each dimension
result_valence <- anova(band.null_valence,band.model)
result_arousal <- anova(band.null_arousal,band.model)

print(result_valence)
print(result_arousal)

# Store results from each dimension in a list
#dimensions_results <- list()
#dimensions_results[[sprintf('%s_valence', b)]] <- result_valence
#dimensions_results[[sprintf('%s_arousal', b)]] <- result_arousal

# Append results from both dimensions to another list, creating a nested list
#bands_results <- append(bands_results, dimensions_results)
#}
#return(bands_results)
#}

frontal_asymmetry_results <- deap_list %>% map(deap_lmm)
names(frontal_asymmetry_results) <- c("offline", "online")
print(frontal_asymmetry_results)
