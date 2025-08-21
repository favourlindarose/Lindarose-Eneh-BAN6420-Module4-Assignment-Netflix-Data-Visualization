# Netflix Shows & Movies Analysis in Python
# Updated to fix deprecated code and improve functionality

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
from datetime import datetime

# Redirect print output to both terminal and file
class Logger(object):
    def __init__(self, filename="analysis_output.txt"):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # This flush method is needed for Python 3 compatibility
        self.terminal.flush()
        if hasattr(self.log, 'flush'):
            self.log.flush()

    def close(self):
        self.log.close()

sys.stdout = Logger("analysis_output.txt")

# ----------------------------
# 1. Data Preparation
# ----------------------------
print("=== Netflix Data Analysis ===\n")
print(f"Analysis date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

filename = "Netflix_shows_movies.csv"

# If dataset doesn't exist, create a more comprehensive dummy one
if not os.path.exists(filename):
    print(f">>> {filename} not found. Creating a sample dataset...\n")
    
    # Create a more realistic sample dataset
    np.random.seed(42)  # For reproducible results
    n_samples = 100
    
    sample_data = {
        "show_id": [f"s{i}" for i in range(1, n_samples+1)],
        "type": np.random.choice(["Movie", "TV Show"], n_samples, p=[0.7, 0.3]),
        "title": [f"Title {i}" for i in range(1, n_samples+1)],
        "director": np.random.choice(["John Doe", "Jane Smith", "Alex Johnson", "Unknown", "Chris Nolan", 
                                    "Ridley Scott", "Unknown Director"], n_samples, p=[0.2, 0.2, 0.1, 0.3, 0.1, 0.05, 0.05]),
        "cast": [f"Actor {chr(65 + i%26)}, Actor {chr(66 + i%26)}" for i in range(n_samples)],
        "country": np.random.choice(["USA", "Canada", "UK", "Nigeria", "India", "France", "Japan", 
                                   "Unknown", "Germany", "Australia"], n_samples),
        "date_added": [f"{np.random.choice(['January', 'February', 'March', 'April', 'May', 'June', 
                                          'July', 'August', 'September', 'October', 'November', 'December'])} "
                      f"{np.random.randint(1, 28)}, {np.random.randint(2015, 2023)}" 
                      for _ in range(n_samples)],
        "release_year": np.random.randint(1990, 2023, n_samples),
        "rating": np.random.choice(["PG", "TV-MA", "R", "PG-13", "TV-14", "TV-PG", "TV-Y", 
                                  "TV-Y7", "G", "NC-17", "UR"], n_samples, 
                                 p=[0.1, 0.2, 0.1, 0.1, 0.15, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05]),
        "duration": [f"{np.random.randint(60, 180)} min" if np.random.random() > 0.3 
                    else f"{np.random.randint(1, 8)} Seasons" for _ in range(n_samples)],
        "listed_in": [np.random.choice(["Dramas", "Comedies", "Action", "Thriller", "Documentaries", 
                                      "International Movies", "Kids' TV", "Romantic Movies"], 2, replace=False) 
                     for _ in range(n_samples)]
    }
    
    # Convert listed_in to string format
    sample_data["listed_in"] = [", ".join(genres) for genres in sample_data["listed_in"]]
    
    df = pd.DataFrame(sample_data)
    df.to_csv(filename, index=False)
    print(f">>> Sample dataset with {n_samples} entries created and saved as {filename}\n")

# Load dataset (either real or dummy)
try:
    df = pd.read_csv(filename)
    print(f">>> Dataset loaded successfully with {len(df)} rows and {len(df.columns)} columns\n")
except Exception as e:
    print(f">>> Error loading dataset: {e}\n")
    sys.exit(1)

# ----------------------------
# 2. Data Cleaning
# ----------------------------
print(">>> Checking missing values before cleaning:")
print(df.isnull().sum(), "\n")

# Fill missing values
df['director'].fillna("Unknown", inplace=True)
df['country'].fillna("Unknown", inplace=True)
df['cast'].fillna("Unknown", inplace=True)

# For date_added, we'll handle it differently
if 'date_added' in df.columns:
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    # Create a new column to indicate if date was parsed correctly
    df['date_added_valid'] = df['date_added'].notna()

# Drop rows with missing rating (if any remain)
initial_count = len(df)
df.dropna(subset=['rating'], inplace=True)
print(f">>> Dropped {initial_count - len(df)} rows with missing ratings\n")

# Extract duration values and convert to numeric where possible
def extract_duration(duration_str):
    if pd.isna(duration_str):
        return np.nan
    if 'min' in str(duration_str):
        return int(''.join(filter(str.isdigit, str(duration_str))))
    elif 'Season' in str(duration_str):
        return int(''.join(filter(str.isdigit, str(duration_str))))
    return np.nan

df['duration_value'] = df['duration'].apply(extract_duration)
df['duration_type'] = df['duration'].apply(
    lambda x: 'min' if 'min' in str(x) else 'Seasons' if 'Season' in str(x) else 'Unknown'
)

# Save cleaned data
df.to_csv("Netflix_shows_movies_cleaned.csv", index=False)
print(">>> Data cleaned and saved to Netflix_shows_movies_cleaned.csv\n")

# ----------------------------
# 3. Data Exploration
# ----------------------------
print(">>> Dataset Info:")
print(df.info(), "\n")

print(">>> Summary Statistics:")
# Handle different pandas versions for describe() method
try:
    # Try newer version first
    print(df.describe(datetime_is_numeric=True, include='all'), "\n")
except TypeError:
    # Fall back to older version if parameter not supported
    print(df.describe(include='all'), "\n")

print(">>> Type Distribution (Movie vs TV Show):")
type_counts = df['type'].value_counts()
print(type_counts, "\n")

print(">>> Ratings Distribution:")
rating_counts = df['rating'].value_counts()
print(rating_counts, "\n")

# Additional analysis
print(">>> Top 10 Countries with most content:")
print(df['country'].value_counts().head(10), "\n")

if 'date_added' in df.columns and df['date_added_valid'].any():
    print(">>> Content added by year:")
    df['year_added'] = df['date_added'].dt.year
    print(df['year_added'].value_counts().sort_index(), "\n")

# ----------------------------
# 4. Data Visualization
# ----------------------------
print(">>> Generating plots...\n")

# Set style for all plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# 1. Type Distribution (Movie vs TV Show)
plt.figure()
type_counts.plot(kind='bar', color=['#E50914', '#221F1F'])  # Netflix colors
plt.title("Distribution of Movies vs TV Shows on Netflix")
plt.xlabel("Content Type")
plt.ylabel("Count")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("type_distribution.png")
plt.close()

# 2. Ratings Distribution - Fixed deprecated syntax
plt.figure()
# Updated syntax to avoid deprecation warning
sns.countplot(data=df, y='rating', hue='rating', order=df['rating'].value_counts().index,
              palette="Reds_r", legend=False)
plt.title("Distribution of Ratings on Netflix")
plt.xlabel("Count")
plt.ylabel("Rating")
plt.tight_layout()
plt.savefig("ratings_distribution.png")
plt.close()

# 3. Top 10 Genres
# First, split the genres which are comma-separated
all_genres = df['listed_in'].str.split(', ').explode()
top_genres = all_genres.value_counts().head(10)

plt.figure()
top_genres.plot(kind='barh', color='#E50914')
plt.title("Top 10 Genres on Netflix")
plt.xlabel("Count")
plt.ylabel("Genre")
plt.tight_layout()
plt.savefig("top_genres.png")
plt.close()

# 4. Content added over time (if date data is available)
if 'year_added' in df.columns:
    plt.figure()
    content_by_year = df['year_added'].value_counts().sort_index()
    content_by_year.plot(kind='line', marker='o', color='#E50914')
    plt.title("Netflix Content Added by Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Titles Added")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("content_added_by_year.png")
    plt.close()

# 5. Duration analysis by type
plt.figure()
movies = df[df['type'] == 'Movie']
tv_shows = df[df['type'] == 'TV Show']

if not movies.empty and 'duration_value' in movies.columns:
    plt.subplot(1, 2, 1)
    plt.hist(movies['duration_value'].dropna(), bins=20, color='#E50914', alpha=0.7)
    plt.title('Movie Duration (minutes)')
    plt.xlabel('Duration (min)')
    plt.ylabel('Count')

if not tv_shows.empty and 'duration_value' in tv_shows.columns:
    plt.subplot(1, 2, 2)
    plt.hist(tv_shows['duration_value'].dropna(), bins=10, color='#221F1F', alpha=0.7)
    plt.title('TV Show Seasons')
    plt.xlabel('Number of Seasons')
    plt.ylabel('Count')

plt.tight_layout()
plt.savefig("duration_analysis.png")
plt.close()

print(">>> Plots saved: type_distribution.png, ratings_distribution.png, top_genres.png, " + 
      ("content_added_by_year.png, duration_analysis.png" if 'year_added' in df.columns else "duration_analysis.png") + "\n")

# ----------------------------
# 5. Additional Insights
# ----------------------------
print(">>> Additional Insights:\n")

# Movies vs TV Shows percentage
total = len(df)
movies_pct = (type_counts.get('Movie', 0) / total) * 100
tv_shows_pct = (type_counts.get('TV Show', 0) / total) * 100
print(f">>> Movies represent {movies_pct:.1f}% of content, TV Shows {tv_shows_pct:.1f}%\n")

# Most common rating
most_common_rating = rating_counts.index[0] if not rating_counts.empty else "N/A"
print(f">>> Most common rating: {most_common_rating}\n")

# Recent content analysis
if 'release_year' in df.columns:
    current_year = datetime.now().year
    df['age'] = current_year - df['release_year']
    avg_age = df['age'].mean()
    print(f">>> Average content age: {avg_age:.1f} years\n")
    
    # Content from last 5 years
    recent_content = df[df['release_year'] >= (current_year - 5)]
    recent_pct = (len(recent_content) / total) * 100
    print(f">>> {recent_pct:.1f}% of content is from the last 5 years\n")

print("=== Analysis Completed ===")

# Close the logger to ensure all output is written
sys.stdout.close()
sys.stdout = sys.stdout.terminal