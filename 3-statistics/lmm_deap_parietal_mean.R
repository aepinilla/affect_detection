library(lme4)
library(tidyverse)

# Define power bands
bands <- list('delta', 'theta', 'alpha', 'beta', 'gamma')

# DEAP dataset preprocessed using offline approach
deap_offline <- read.csv("../features/deap_offline_features.csv")

# DEAP dataset preprocessed using online approach
deap_online <- read.csv("../features/deap_online_features.csv")

# Add preprocessing type label to each dataset
deap_offline <- deap_offline %>% mutate(preprocessing = 'offline')
deap_online <- deap_online %>% mutate(preprocessing = 'online')

# Create list with both datasets
deap_list <- list(deap_offline, deap_online)

# Define linear mixed models function
deap_lmm <- function(deap_data) {
  # Create empty vector to store results from each power band
  bands_results <- vector()
  for (b in bands) {
    # Subset data from current power band
    band_data <- deap_data %>%
      filter(band == b)
    
    # Build full model
    band.model = lmer(parietal_mean ~ valence_rating + arousal_rating +
                        (1+valence_rating|participant) +
                        (1+valence_rating|video_id) +
                        (1+arousal_rating|participant) +
                        (1+arousal_rating|video_id),
                      data=band_data,
                      REML=FALSE)
    
    
    # Build reduced model without valence ratings
    band.null_valence = lmer(parietal_mean ~ arousal_rating +
                               (1+valence_rating|participant) +
                               (1+valence_rating|video_id) +
                               (1+arousal_rating|participant) +
                               (1+arousal_rating|video_id),
                             data=band_data,
                             REML=FALSE)

    # Build reduced model without arousal ratings
    band.null_arousal = lmer(parietal_mean ~ valence_rating +
                               (1+valence_rating|participant) +
                               (1+valence_rating|video_id) +
                               (1+arousal_rating|participant) +
                               (1+arousal_rating|video_id),
                             data=band_data,
                             REML=FALSE)

    # Obtain likelihood ratio for valence dimension
    result_valence <- anova(band.null_valence,band.model)

    # Obtain likelihood ratio for arousal dimension
    result_arousal <- anova(band.null_arousal,band.model)

    # Store results from each dimension in a list
    dimensions_results <- list()
    dimensions_results[[sprintf('%s_valence', b)]] <- result_valence
    dimensions_results[[sprintf('%s_arousal', b)]] <- result_arousal

    # Append results from both dimensions to another list, creating a nested list
    bands_results <- append(bands_results, dimensions_results)
  }
  return(bands_results)
}

parietal_mean_results <- deap_list %>% map(deap_lmm)
names(parietal_mean_results) <- c("offline", "online")
print(parietal_mean_results)

