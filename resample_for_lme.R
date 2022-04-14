library(lme4)
library(tidyverse)

setwd("~/Documents/MATLAB/affect_detection/features")

# Create list of files
files_list <- list.files()

# Define bands
bands <- list('delta', 'theta', 'alpha', 'beta', 'gamma')

# Define video ids
# Define video codes
video_ids <- list('aem',
                  'bbs',
                  'blf',
                  'bls',
                  'cah',
                  'dph',
                  'goc',
                  'gam',
                  'jbg',
                  'jmi',
                  'mar',
                  'mcm',
                  'ndp',
                  'ser',
                  'tsl',
                  'tsd')

# Define reduction factor
n <- 95

# Reduce sampling rate for faster computer processing
all_files <- list()

for (file in 1:length(files_list)) {
  file_data <- read.csv(files_list[file])
  all_videos <- list()
  for (video in 1:length(video_ids)) {
    video_data <- file_data %>% filter(video_id == video_ids[video])
    all_bands <- list()
    for (b in bands) {
      band_data = video_data %>% filter(band == b)
      
      reduced_band_video_data <- aggregate(band_data, list(rep(1:(nrow(band_data) %/% n + 1), each = n, len = nrow(band_data))), mean)[-1];
      reduced_band_video_data$gender <- band_data$gender[1]
      reduced_band_video_data$band <- band_data$band[1]
      reduced_band_video_data$second <- 1:60
      reduced_band_video_data$participant <- band_data$participant[1]
      reduced_band_video_data$video_id <- band_data$video_id[1]
        
      all_bands <- bind_rows(all_bands, reduced_band_video_data)
    }
    all_videos <- bind_rows(all_videos, all_bands)
    write.csv(all_videos, file = paste("~/Documents/MATLAB/affect_detection/lme_features/",band_data$participant[1],".csv", sep = ""), row.names = FALSE)
  }
}
