# netflix_analysis.R
# Netflix Data Visualization in R
# Integration with Python analysis

# Install required packages if not already installed
if (!require(ggplot2)) install.packages("ggplot2")
if (!require(dplyr)) install.packages("dplyr")
if (!require(readr)) install.packages("readr")
if (!require(tidyr)) install.packages("tidyr")

library(ggplot2)
library(dplyr)
library(readr)
library(tidyr)

# Set output file
sink("r_analysis_output.txt", append = FALSE, split = TRUE)

cat("=== NETFLIX DATA VISUALIZATION IN R ===\n\n")
cat("Analysis date:", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n\n")

# Check if cleaned data exists
if (!file.exists("Netflix_shows_movies_cleaned.csv")) {
  cat("ERROR: Cleaned data file not found. Please run the Python script first.\n")
  sink()
  stop("Required data file missing")
}

cat("1. Loading cleaned data...\n")
netflix_data <- read_csv("Netflix_shows_movies_cleaned.csv")

cat("Dataset loaded successfully with", nrow(netflix_data), "rows and", ncol(netflix_data), "columns\n\n")

# Basic data exploration
cat("2. Data Exploration:\n")
cat("Dataset structure:\n")
print(str(netflix_data))
cat("\n")

cat("Summary statistics:\n")
print(summary(netflix_data))
cat("\n")

cat("Content type distribution:\n")
print(table(netflix_data$type))
cat("\n")

cat("Rating distribution:\n")
print(table(netflix_data$rating))
cat("\n")

# 3. Data Visualization
cat("3. Creating visualizations...\n")

# Most watched genres visualization
cat("-> Creating most watched genres visualization...\n")
genre_data <- netflix_data %>%
  separate_rows(listed_in, sep = ", ") %>%
  count(listed_in, sort = TRUE) %>%
  head(10)

p1 <- ggplot(genre_data, aes(x = reorder(listed_in, n), y = n)) +
  geom_bar(stat = "identity", fill = "#E50914", alpha = 0.8) +
  coord_flip() +
  labs(title = "Top 10 Most Watched Genres on Netflix",
       subtitle = "Based on content availability",
       x = "Genre",
       y = "Number of Titles") +
  theme_minimal() +
  theme(plot.title = element_text(face = "bold", size = 16, color = "#E50914"),
        plot.subtitle = element_text(size = 12),
        axis.title = element_text(face = "bold"),
        panel.grid.major.y = element_blank())

ggsave("most_watched_genres_r.png", p1, width = 12, height = 8, dpi = 300)

# Ratings distribution visualization
cat("-> Creating ratings distribution visualization...\n")
rating_data <- netflix_data %>%
  count(rating, sort = TRUE)

p2 <- ggplot(rating_data, aes(x = reorder(rating, n), y = n)) +
  geom_bar(stat = "identity", fill = "#221F1F", alpha = 0.8) +
  coord_flip() +
  labs(title = "Distribution of Ratings on Netflix",
       x = "Rating",
       y = "Number of Titles") +
  theme_minimal() +
  theme(plot.title = element_text(face = "bold", size = 16, color = "#221F1F"),
        axis.title = element_text(face = "bold"),
        panel.grid.major.y = element_blank())

ggsave("ratings_distribution_r.png", p2, width = 10, height = 8, dpi = 300)

# Content type pie chart
cat("-> Creating content type visualization...\n")
type_data <- netflix_data %>%
  count(type)

p3 <- ggplot(type_data, aes(x = "", y = n, fill = type)) +
  geom_bar(stat = "identity", width = 1) +
  coord_polar("y", start = 0) +
  scale_fill_manual(values = c("#E50914", "#221F1F")) +
  labs(title = "Content Type Distribution on Netflix",
       fill = "Content Type") +
  theme_void() +
  theme(plot.title = element_text(face = "bold", size = 16, hjust = 0.5),
        legend.position = "bottom")

ggsave("content_type_r.png", p3, width = 10, height = 8, dpi = 300)

# Additional visualization: Content added over time
if ("year_added" %in% colnames(netflix_data)) {
  cat("-> Creating content timeline visualization...\n")
  yearly_data <- netflix_data %>%
    filter(!is.na(year_added)) %>%
    count(year_added)
  
  p4 <- ggplot(yearly_data, aes(x = year_added, y = n)) +
    geom_line(color = "#E50914", size = 1.5) +
    geom_point(color = "#E50914", size = 3) +
    labs(title = "Netflix Content Added by Year",
         x = "Year",
         y = "Number of Titles Added") +
    theme_minimal() +
    theme(plot.title = element_text(face = "bold", size = 16, color = "#E50914"),
          axis.title = element_text(face = "bold"))
  
  ggsave("content_timeline_r.png", p4, width = 12, height = 8, dpi = 300)
}

cat("4. Additional Insights:\n\n")

# Calculate percentages
total_titles <- nrow(netflix_data)
movies_pct <- round(sum(netflix_data$type == "Movie") / total_titles * 100, 1)
tv_shows_pct <- round(sum(netflix_data$type == "TV Show") / total_titles * 100, 1)

cat("Content Type Distribution:\n")
cat("- Movies:", movies_pct, "%\n")
cat("- TV Shows:", tv_shows_pct, "%\n\n")

# Most common rating
most_common_rating <- names(sort(table(netflix_data$rating), decreasing = TRUE))[1]
cat("Most common rating:", most_common_rating, "\n\n")

# Recent content analysis
if ("release_year" %in% colnames(netflix_data)) {
  current_year <- as.numeric(format(Sys.Date(), "%Y"))
  recent_content <- sum(netflix_data$release_year >= (current_year - 5), na.rm = TRUE)
  recent_pct <- round(recent_content / total_titles * 100, 1)
  
  cat("Recent Content Analysis:\n")
  cat("- Content from last 5 years:", recent_pct, "%\n")
  cat("- Average content age:", round(mean(current_year - netflix_data$release_year, na.rm = TRUE), 1), "years\n\n")
}

cat("5. Files Generated:\n")
cat("- most_watched_genres_r.png: Top genres visualization\n")
cat("- ratings_distribution_r.png: Ratings distribution\n")
cat("- content_type_r.png: Content type pie chart\n")
if ("year_added" %in% colnames(netflix_data)) {
  cat("- content_timeline_r.png: Content addition timeline\n")
}
cat("- r_analysis_output.txt: This analysis report\n\n")

cat("=== R ANALYSIS COMPLETED SUCCESSFULLY ===\n")
cat("All visualizations have been saved as PNG files.\n")

sink()

# Print completion message to console
cat("R analysis completed. Check the generated PNG files and r_analysis_output.txt\n")