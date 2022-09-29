# Install packages if required
if(!require(tidyverse)){install.packages("tidyverse")}
if(!require(dplyr)){install.packages("dplyr")}
if(!require(lme4)){install.packages("lme4")}
if(!require(arrow)){install.packages("arrow")}

# Load packages
library(tidyverse)
library(dplyr)
library(lme4)
library(arrow)

#########################################
# EDIT ACCORDING TO YOUR WORKING DIRECTORY
working_directory <- "~/Documents/MATLAB/affect_detection/reports/feature_selection/lme/base/"
#########################################

setwd(working_directory)

# Create list of files
# participants_list <- list.files()
participants_list <- c("DODE8.csv", "SDE14.csv")
len_participants_list <- seq(1, length(participants_list))

# # Define variables
iterations <- seq(1, 10)
dimensions <- list('negativity_rating', 'positivity_rating', 'net_predisposition_rating')
features <- list('spectral_envelope',
                 'zero_crossings',
                 'katz_fractal_dimension',
                 'hjorth_activity',
                 'hjorth_movility',
                 'hjorth_complexity',
                 'petrosian_fractal_dimension')


# Full model function
build_full_model <- function(dimension, feature, df) {
  dimension.model = lmer(get(dimension) ~ get(feature) + ts +
                           (1+get(feature)|video_id),
                         REML=FALSE,
                         data = df,
                         control = lmerControl(calc.derivs = FALSE))
  return (dimension.model)
}


# Null model function
build_null_model <- function(dimension, feature, df) {
  dimension.null = lmer(get(dimension) ~ ts +
                          (1+get(feature)|video_id),
                        REML=FALSE,
                        data = df,
                        control = lmerControl(calc.derivs = FALSE))
  return (dimension.null)
}


# Select data function
select_data <- function(data, iteration_trials, dimension, electrode_site) {
  if (dimension == 'negativity_rating') {
    negativity_trials <- iteration_trials$negativity
    subset <- data %>%
      filter(electrode == electrode_site,
             data$trial == negativity_trials)
  } else if (dimension == 'positivity_rating') {
    positivity_trials <- iteration_trials$positivity
    subset <- data %>%
      filter(electrode == electrode_site,
             data$trial == positivity_trials)
  } else if (dimension == 'net_predisposition_rating') {
    net_predisposition_trials <- iteration_trials$net_predisposition
    subset <- data %>%
      filter(electrode == electrode_site,
             data$trial == net_predisposition_trials)
  }
  
  return (subset)
}


"Run analysis on each participant:
This technique aims to build user-dependent affect detection models.
Consequently, feature selection should be conducted with the data of each
participant."
for (p in len_participants_list) {
  print(paste('Analysing participant',p,sep = " "))
  participant_data <- read.csv(participants_list[p])
  participant_code <- substr(participants_list[p], 1,5)
  participant_results <- list()
  electrodes <- unique(participant_data$electrode)
  
  # Load random trials indices
  random_trials_file_path <- paste('~/Documents/MATLAB/affect_detection/reports/random_indices/', participants_list[p], sep = "")
  random_trials_indices <- read.csv(random_trials_file_path)
  # Run 10 iterations. Each iteration is run with a different random selection of trials.
  for (i in iterations) {
    print(paste('Running iteration', i, sep = " "))
    iteration_trials <- random_trials_indices %>%
      filter(iteration == i)
    
    "Run once on each affective dimension:
    Affective dimensions are conceptually independent constructs. Therefore, one
    model should be built for each dimension. Consequently, feature selection must
    be conducted independently for each dimension as well."
    for (d in dimensions) {
      print(paste('Analysing',d,sep = " "))
      "Run once on each electrode site"
      for (e in electrodes) {
        subset_df <- select_data(participant_data, iteration_trials, d, e)
        for (f in features) {
          print(paste('Analysing',f,'at electrode site',e,sep = " "))
          # Build full model
          full_model <- try(build_full_model(dimension = d, feature = f, df = subset_df))
          # Build null model
          null_model <- try(build_null_model(dimension = d, feature = f, df = subset_df))
          # Check whether both models were built. In some cases, models cannot be built.
          # Some models cannot be built because 'Downdated VtV is not positive definite'".
          if ((class(null_model) == 'lmerMod')  & (class(full_model) == 'lmerMod')) {
            # ... conduct a likelihood-ratio test
            result <- anova(null_model, full_model)
            # assign participant code and feature name
            result$participant <- participant_code
            result$iteration <- i
            result$dimension <- d
            result$electrode <- e
            result$feature <- f
            # # Save the entire table with all the details
            participant_results[[sprintf('%s_%s_%s_%s', i, d, e, f)]] <- result
            # Remove models before next iteration
            rm(full_model)
            rm(null_model)
          }
        }
      }
    }
    
    # Define the directory where results are going to be exported
    export_path = paste(working_directory, participant_code, sep = "")
    
    # Export results in Feather format, which can be easily read as a Pandas dataframe in Python
    sapply(seq_along(1:length(participant_results)), 
           function(n) write_feather(participant_results[[n]], 
                                     paste(export_path,"_base_",i,'_',n,".feather", sep = "")))
  }
}
