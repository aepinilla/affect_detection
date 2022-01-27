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
      dimension.model = lmer(get(f) ~ get(d) +
                               (1+get(d)|participant) +
                               (1+get(d)|video_id) +
                               (1+get(d)|second),
                             REML=FALSE,
                             data = band_data,
                             control = lmerControl(calc.derivs = FALSE))
      
      # Assumptions plots
      plot_title <- sprintf('%s_%s_%s', d, b, f)
      
      jpeg(sprintf('../figures/assumptions/%s_residuals.jpg', plot_title))
      plot(fitted(dimension.model), jitter(residuals(dimension.model), 1000))
      title(sub = plot_title)
      dev.off()
      
      jpeg(sprintf('../figures/assumptions/%s_hist.jpg', plot_title))
      hist(residuals(dimension.model))
      title(sub = plot_title)
      dev.off()

      jpeg(sprintf('../figures/assumptions/%s_qqnorm.jpg', plot_title))
      qqnorm(residuals(dimension.model))
      title(sub = plot_title)
      dev.off()
    }
  }
}

