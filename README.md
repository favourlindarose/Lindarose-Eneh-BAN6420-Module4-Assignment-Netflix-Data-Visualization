````markdown
# Netflix Data Visualization Analysis

This project provides a comprehensive analysis of Netflix shows and movies data using both **Python** and **R** for data visualization.

---

## Assignment Requirements Met
- **Data Preparation**: Unzipping and renaming dataset  
- **Data Cleaning**: Handling missing values appropriately  
- **Data Exploration**: Statistical analysis and data description  
- **Data Visualization**: Creating visualizations for:
  - Most watched genres  
  - Ratings distribution  
- **R Integration**: Implementing visualizations in R  

---

## Files Included
- `netflix_analysis.py`: Python implementation of the analysis  
- `netflix_analysis.R`: R implementation of the analysis  
- `README.md`: This instruction file  
- Sample data will be generated if no Netflix dataset is provided  

---

## How to Use

### Python Analysis
1. Ensure you have Python installed with the required libraries:  
   ```bash
   pip install pandas numpy matplotlib seaborn
````

2. Place your Netflix data CSV file (`Netflix_shows_movies.csv`) in the same directory.

   * If not provided, the script will generate sample data.
3. Run the Python script:

   ```bash
   analysis.py
   ```

The script will:

* Generate sample data if needed
* Clean the data by handling missing values
* Perform exploratory data analysis
* Create visualizations (saved as PNG files)
* Export cleaned data for R analysis

---

### R Analysis

1. Ensure you have R installed with the required packages:

   * `ggplot2`
   * `dplyr`
   * `tidyr`
   * `readr`

2. First run the Python script to generate the cleaned data.

3. Run the R script:

   ```bash
   Rscript analysis.R
   ```

The script will:

* Read the cleaned data prepared by Python
* Create visualizations (saved as PNG files)
* Generate a summary report

---

## Output Files

### Python Outputs

* `Netflix_shows_movies_cleaned.csv`: Cleaned dataset
* `type_distribution.png`: Movies vs TV Shows distribution
* `ratings_distribution.png`: Ratings distribution chart
* `top_genres.png`: Top 10 genres visualization
* `content_added_by_year.png`: Content timeline (if date data available)
* `duration_analysis.png`: Duration analysis by content type
* `analysis_output.txt`: Summary output from Python analysis

### R Outputs

* `most_watched_genres_r.png`: Top genres visualization
* `ratings_distribution_r.png`: Ratings distribution
* `content_type_r.png`: Content type pie chart
* `content_timeline_r.png`: Content addition timeline (if date data available)
* `r_analysis_output.txt`: Summary output from R analysis

---

## Visualizations Created

### Python Visualizations

* Distribution of Movies vs TV Shows (bar chart)
* Distribution of Ratings (count plot)
* Top 10 Genres (horizontal bar chart)
* Content Added by Year (line chart, if date data available)
* Duration Analysis by Content Type (histograms)

### R Visualizations

* Top 10 Most Watched Genres (horizontal bar chart)
* Distribution of Ratings (bar chart)
* Content Type Distribution (pie chart)
* Netflix Content Added by Year (line chart, if date data available)

---

## Notes

* If no Netflix dataset is provided, the Python script will generate a sample dataset with 100 entries for demonstration.
* The analysis handles missing values appropriately by either filling them or removing problematic rows.
* Both Python and R scripts include error handling to ensure smooth execution.

---

## Dependencies

### Python

* pandas
* numpy
* matplotlib
* seaborn

### R

* ggplot2
* dplyr
* tidyr
* readr

---

## How to Run the Complete Analysis

1. Save all files in the same directory:

   * `analysis.py`
   * `analysis.R`

2. Run the Python script first:

   ```bash
   python analysis.py
   ```

3. Then run the R script:

   ```bash
   Rscript analysis.R
   ```

4. Check the generated visualizations and output files.
