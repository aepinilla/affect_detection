library(lme4)
library(tidyverse)

setwd("~/Documents/MATLAB/affect_detection/features")

# Create list of files
files_list <- list.files()

# Concatenate all files
all_files <- list()
for (file in 1:length(files_list)) {
  file_data <- read.csv(files_list[file])
  all_files <- bind_rows(all_files, file_data)
}

# Define variables
dimensions <- list('negativity_rating', 'positivity_rating', 'net_predisposition_rating')
features <- list('frontal_asymmetry', 'parietal_mean')
bands <- list('delta', 'theta', 'alpha', 'beta', 'gamma')

all_results <- list()
for (d in dimensions) {
  for (f in features) {
    for (b in bands) {
      # Subset data from current power band
      band_data <- all_files %>%
        filter(band == b)
      
      # Build full model
      dimension.model = lmer(get(d) ~ get(f) +
                                (1+get(f)|participant) + gender +
                                (1+get(f)|video_id) +
                                (1+get(f)|second),
                              REML=FALSE,
                              data = band_data,
                              control = lmerControl(calc.derivs = FALSE))
      
      # Build null model
      dimension.null = lmer(get(d) ~
                               (1+get(f)|participant) + gender +
                               (1+get(f)|video_id) +
                               (1+get(f)|second),
                             REML=FALSE,
                             data = band_data,
                             control = lmerControl(calc.derivs = FALSE))

      # Obtain likelihood ratio for negativity dimension
      result <- anova(dimension.null, dimension.model)
      all_results[[sprintf('%s_%s_%s', d, b, f)]] <- result
    }
  }
}

capture.output(all_results, file = "~/Documents/MATLAB/affect_detection/results/lmm_results.txt")
print(all_results)

