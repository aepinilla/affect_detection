library(lme4)
library(tidyverse)
library(sjPlot)
library(Cairo)
library(ggplot2)
theme_set(theme_sjplot())


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

# Add labels
attr(all_files$participant, "label") <- "Participant"
attr(all_files$video_id, "label") <- "Video"
attr(all_files$second, "label") <- "Seconds"
attr(all_files$band, "label") <- "Power band"
attr(all_files$frontal_asymmetry, "label") <- "Frontal asymmetry"
attr(all_files$parietal_mean, "label") <- "Mean parietal power"
attr(all_files$negativity_rating, "label") <- "Negativity rating"
attr(all_files$positivity_rating, "label") <- "Positivity rating"
attr(all_files$net_predisposition_rating, "label") <- "Net predisposition rating"

for (d in dimensions) {
  for (b in bands) {
    # Subset data from current power band
    band_data <- all_files %>%
      filter(band == b)

    # Define axis label
    attr(band_data$frontal_asymmetry, "label") <- paste("Frontal", b, "asymmetry")

    # Build full model
    dimension.model = lmer(get(d) ~ frontal_asymmetry + gender +
                             (1+frontal_asymmetry|participant) +
                             (1+frontal_asymmetry|video_id) +
                             (1+frontal_asymmetry|second),
                           REML=FALSE,
                           data = band_data,
                           control = lmerControl(calc.derivs = FALSE))

    # Fixed effect plot
    plot_title <- sprintf('%s_%s_frontal', d, b)
    setEPS()
    postscript(sprintf('../figures/fixed_effects/frontal/%s_fixed_effect.eps', plot_title))
    p <- plot_model(dimension.model, type = "slope") + ylim(0,10) + xlim(-40,30)
    print(p)
    dev.off()
  }
}

for (d in dimensions) {
  for (b in bands) {
    # Subset data from current power band
    band_data <- all_files %>%
      filter(band == b)
    
    # Define axis label
    attr(band_data$parietal_mean, "label") <- paste("Mean parietal", b, "power")
    
    # Build full model
    dimension.model = lmer(get(d) ~ parietal_mean + gender +
                             (1+parietal_mean|participant) +
                             (1+parietal_mean|video_id) +
                             (1+parietal_mean|second),
                           REML=FALSE,
                           data = band_data,
                           control = lmerControl(calc.derivs = FALSE))
    
    # Fixed effect plot
    plot_title <- sprintf('%s_%s_parietal', d, b)
    setEPS()
    postscript(sprintf('../figures/fixed_effects/parietal/%s_fixed_effect.eps', plot_title))
    p <- plot_model(dimension.model, type = "slope") + ylim(0,10) + xlim(0,100)
    print(p)
    dev.off()
  }
}



