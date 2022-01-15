library(lme4)
library(tidyverse)
library(sjPlot)
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

# delta plots
b = 'delta'
delta_data <- all_files %>%
  filter(band == b)
attr(delta_data$frontal_asymmetry, "label") <- paste("Frontal", b, "asymmetry")
delta_fa.model = lmer(frontal_asymmetry ~ negativity_rating + positivity_rating + net_predisposition_rating +
                    (1+negativity_rating|participant) +
                    (1+negativity_rating|video_id) +
                    (1+negativity_rating|second),
                  REML=FALSE,
                  data = delta_data,
                  control = lmerControl(calc.derivs = FALSE))
  
plot_model(delta_fa.model, type = "slope")
plot_model(delta_fa.model, type = "re")

attr(delta_data$parietal_mean, "label") <- paste("Mean parietal", b, "power")
delta_pm.model = lmer(parietal_mean ~ negativity_rating + positivity_rating + net_predisposition_rating +
                        (1+negativity_rating|participant) +
                        (1+negativity_rating|video_id) +
                        (1+negativity_rating|second),
                      REML=FALSE,
                      data = delta_data,
                      control = lmerControl(calc.derivs = FALSE))

plot_model(delta_pm.model, type = "slope")
plot_model(delta_pm.model, type = "re")

# theta plots
b = 'theta'
theta_data <- all_files %>%
  filter(band == b)
attr(theta_data$frontal_asymmetry, "label") <- paste("Frontal", b, "asymmetry")
theta_fa.model = lmer(frontal_asymmetry ~ negativity_rating + positivity_rating + net_predisposition_rating +
                    (1+negativity_rating|participant) +
                    (1+negativity_rating|video_id) +
                    (1+negativity_rating|second),
                  REML=FALSE,
                  data = theta_data,
                  control = lmerControl(calc.derivs = FALSE))

plot_model(theta_fa.model, type = "slope")
plot_model(theta_fa.model, type = "re")

attr(theta_data$parietal_mean, "label") <- paste("Mean parietal", b, "power")
theta_pm.model = lmer(parietal_mean ~ negativity_rating + positivity_rating + net_predisposition_rating +
                        (1+negativity_rating|participant) +
                        (1+negativity_rating|video_id) +
                        (1+negativity_rating|second),
                      REML=FALSE,
                      data = theta_data,
                      control = lmerControl(calc.derivs = FALSE))

plot_model(theta_pm.model, type = "slope")
plot_model(theta_pm.model, type = "re")

# alpha plots
b = 'alpha'
alpha_data <- all_files %>%
  filter(band == b)
attr(alpha_data$frontal_asymmetry, "label") <- paste("Frontal", b, "asymmetry")
alpha_fa.model = lmer(frontal_asymmetry ~ negativity_rating + positivity_rating + net_predisposition_rating +
                    (1+negativity_rating|participant) +
                    (1+negativity_rating|video_id) +
                    (1+negativity_rating|second),
                  REML=FALSE,
                  data = alpha_data,
                  control = lmerControl(calc.derivs = FALSE))

plot_model(alpha_fa.model, type = "slope")
plot_model(alpha_fa.model, type = "re")

attr(alpha_data$parietal_mean, "label") <- paste("Mean parietal", b, "power")
alpha_pm.model = lmer(parietal_mean ~ negativity_rating + positivity_rating + net_predisposition_rating +
                        (1+negativity_rating|participant) +
                        (1+negativity_rating|video_id) +
                        (1+negativity_rating|second),
                      REML=FALSE,
                      data = alpha_data,
                      control = lmerControl(calc.derivs = FALSE))

plot_model(alpha_pm.model, type = "slope")
plot_model(alpha_pm.model, type = "re")


# beta plots
b = 'beta'
beta_data <- all_files %>%
  filter(band == b)
attr(beta_data$frontal_asymmetry, "label") <- paste("Frontal", b, "asymmetry")
beta_fa.model = lmer(frontal_asymmetry ~ negativity_rating + positivity_rating + net_predisposition_rating +
                    (1+negativity_rating|participant) +
                    (1+negativity_rating|video_id) +
                    (1+negativity_rating|second),
                  REML=FALSE,
                  data = beta_data,
                  control = lmerControl(calc.derivs = FALSE))

plot_model(beta_fa.model, type = "slope")
plot_model(beta_fa.model, type = "re")

attr(beta_data$parietal_mean, "label") <- paste("Mean parietal", b, "power")
beta_pm.model = lmer(parietal_mean ~ negativity_rating + positivity_rating + net_predisposition_rating +
                       (1+negativity_rating|participant) +
                       (1+negativity_rating|video_id) +
                       (1+negativity_rating|second),
                     REML=FALSE,
                     data = beta_data,
                     control = lmerControl(calc.derivs = FALSE))

plot_model(beta_pm.model, type = "slope")
plot_model(beta_pm.model, type = "re")

# gamma plots
b = 'gamma'
gamma_data <- all_files %>%
  filter(band == b)
attr(gamma_data$frontal_asymmetry, "label") <- paste("Frontal", b, "asymmetry")
gamma_fa.model = lmer(frontal_asymmetry ~ negativity_rating + positivity_rating + net_predisposition_rating +
                    (1+negativity_rating|participant) +
                    (1+negativity_rating|video_id) +
                    (1+negativity_rating|second),
                  REML=FALSE,
                  data = gamma_data,
                  control = lmerControl(calc.derivs = FALSE))

plot_model(gamma_fa.model, type = "slope")
plot_model(gamma_fa.model, type = "re")

attr(gamma_data$parietal_mean, "label") <- paste("Mean parietal", b, "power")
gamma_pm.model = lmer(parietal_mean ~ negativity_rating + positivity_rating + net_predisposition_rating +
                        (1+negativity_rating|participant) +
                        (1+negativity_rating|video_id) +
                        (1+negativity_rating|second),
                      REML=FALSE,
                      data = gamma_data,
                      control = lmerControl(calc.derivs = FALSE))

plot_model(gamma_pm.model, type = "slope")
plot_model(gamma_pm.model, type = "re")
