# Recipe Clustering Logic

# This page handles the machine learning aspect of the application.
# It uses K-Means clustering to group similar recipes together based on their ingredients.
# Process for clustering: 
# 1. Convert recipe ingredients into numerical vectors (feature extraction)
# 2. Apply K-Means clustering to group similar recipes
# 3. Calculate popularity scores for each cluster
# 4. Use these clusters to boost recommendations

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os
import sqlite3

# Creating a class that handles recipe clustering using K-Means algorithm.
class RecipeClusterer:
    # Attributes:
    # recipes_df : the loaded recipes dataset
    # n_clusters : integer number of clusters to create (default: 5)
    # kmeans_model : KMeans = the trained K-Means model
    # scaler : Scaler for normalizing features
    # feature_vectors : numerical representation of recipes (ndarray)
    # cluster_popularity : popularity score for each cluster (dictionnary)
    
# Initializing the RecipeClusterer
    def __init__(self, db_path, n_clusters=5):
        
        # Parameters:
        # - db_path : str, path to the recipes SQLite database file
        # - n_clusters : int, number of recipe clusters to create (5)

        # We use 5 clusters as a default because it provides a good balance:
        # - Not too few (which would group very different recipes together)
        # - Not too many (which would split similar recipes apart)
    
        self.n_clusters = n_clusters # stores how many clusters to create
        self.recipes_df = None # placeholder for the recipes DataFrame
        self.kmeans_model = None # placeholder for the fitted KMeans model
        self.scaler = StandardScaler() #  instantiate a StandardScaler to normalize feature vectors
        self.feature_vectors = None # placeholder for the numerical ingredient vectors before/after scaling
        self.cluster_popularity = {} # dict to hold per-cluster popularity scores after they’re computed

        # Load the recipes dataset
        self._load_recipes(db_path)

        # Process ingredients and create feature vectors
        self._create_feature_vectors()

        # Train the clustering model
        self._train_clustering_model()

        # Calculate cluster-level popularity
        self._calculate_cluster_popularity()

# METHOD DEFINITION

    # Using Pandas to load the SQLite file 
    # Loading recipes from Dataset 
    def _load_recipes(self, db_path):

        if not os.path.exists(db_path): # Error handling
            raise FileNotFoundError(f"Recipe database not found at: {db_path}")

        # Load SQLite table into a pandas DataFrame
        with sqlite3.connect(db_path) as conn:
            self.recipes_df = pd.read_sql("SELECT * FROM recipes", conn)

        # Convert ingredients from string to list
        # DB stores lists as strings like "Eggs,Milk,Flour" and we need to convert them to Python lists: ["Eggs", "Milk", "Flour"]
        self.recipes_df['ingredients'] = self.recipes_df['ingredients'].apply(
            lambda x: [ing.strip() for ing in x.split(',')]
        )

        print(f"Loaded {len(self.recipes_df)} recipes from dataset")
    # Convert recipe ingredients into numerical feature vectors, as ML works with numbers
    def _create_feature_vectors(self):
        # This method= 
        # collects all unique ingredients, one-hot encodes each recipe into a binary vector, converts to a NumPy array, and scales the features with StandardScaler so all dimensions have comparable scale.

        # One-Hot Encoding
        # For each recipe, we create a binary vector where:
        #- 1 means the ingredient is in the recipe
        #- 0 means the ingredient is NOT in the recipe

        # 1) get a list of ALL unique ingredients across all recipes
        all_ingredients = set()
        for ingredients in self.recipes_df['ingredients']:
            all_ingredients.update(ingredients)

        # 2) sort for consistency
        all_ingredients = sorted(list(all_ingredients))
        print(f"Found {len(all_ingredients)} unique ingredients")

        # 3) create feature vectors using one-hot encoding
        feature_vectors = []

        for ingredients in self.recipes_df['ingredients']:
            # Create a binary vector for this recipe
            vector = [1 if ing in ingredients else 0 for ing in all_ingredients]
            feature_vectors.append(vector)

        # Convert to numpy array for sklearn
        self.feature_vectors = np.array(feature_vectors)

        # Normalize the features using StandardScaler
        # This ensures all features have similar scales (mean=0, std=1), because K-Means is sensitive to feature scales
        self.feature_vectors = self.scaler.fit_transform(self.feature_vectors)

        print(f"Created feature vectors of shape: {self.feature_vectors.shape}")

    # Train the clustering model
    def _train_clustering_model(self):
        
        # Initialize K-Means with our desired number of clusters
        self.kmeans_model = KMeans(
            n_clusters=self.n_clusters,
            random_state=42,  # For reproducibility (same results every time)
            n_init=10,  # Number of times to run with different initial centers
            max_iter=300  # Maximum iterations for convergence
        )

        # Train the model on our feature vectors
        # This finds the optimal cluster assignments
        self.kmeans_model.fit(self.feature_vectors)

        # Add cluster assignments to our DataFrame - so that each recipe knows which cluster it belongs to.
        self.recipes_df['cluster_id'] = self.kmeans_model.labels_

        print(f"Trained K-Means model with {self.n_clusters} clusters")

        # Show how many recipes are in each cluster
        cluster_counts = self.recipes_df['cluster_id'].value_counts().sort_index()
        print("\n Recipes per cluster:")
        for cluster_id, count in cluster_counts.items():
            print(f"  Cluster {cluster_id}: {count} recipes")

    # Cluster popularity calculation:average rating of all recipes in that cluster.
    # If a cluster contains highly-rated recipes, it's a "popular" cluster. --> to boost recomendations
    def _calculate_cluster_popularity(self):

        # cluster_popularity = mean(ratings of all recipes in cluster) --> We then normalize this to a 0-1 scale for easier combining with other scores.

        # Calculate average rating per cluster.
        for cluster_id in range(self.n_clusters):
            # Get all recipes in this cluster
            cluster_recipes = self.recipes_df[self.recipes_df['cluster_id'] == cluster_id]

            # Calculate average rating
            avg_rating = cluster_recipes['rating'].mean()

            # Store in our dictionary
            self.cluster_popularity[cluster_id] = avg_rating

        # Normalize to 0-1 scale
        # This makes it easier to combine with other scores later
        min_pop = min(self.cluster_popularity.values()) 
        max_pop = max(self.cluster_popularity.values())
        # Finding the highest and lowest popularity values currently in self.cluster_popularity (the per cluster average)

        for cluster_id in self.cluster_popularity:
            if max_pop > min_pop:
                # Normalize: (value - min) / (max - min)
                normalized = (self.cluster_popularity[cluster_id] - min_pop) / (max_pop - min_pop)
                self.cluster_popularity[cluster_id] = normalized
            else:
                # If all clusters have same popularity, set to 0.5
                self.cluster_popularity[cluster_id] = 0.5
        print(f"\n Calculated cluster popularity scores:")

        for cluster_id, pop in self.cluster_popularity.items():
            print(f"   Cluster {cluster_id}: {pop:.3f}")

    # Get the cluster ID for a specific recipe
    def get_recipe_cluster(self, recipe_name):
        # Parameters:
        # recipe_name : Name of the recipe (str)
        # Returns: int or None
        # = Cluster ID if recipe found, None otherwise
        recipe = self.recipes_df[self.recipes_df['recipe_name'] == recipe_name]
        if len(recipe) > 0:
            return int(recipe.iloc[0]['cluster_id'])
        return None

    # Get the popularity score for a cluster.
    def get_cluster_popularity(self, cluster_id):
        # Parameters:
        # cluster_id : The cluster ID (int)
        # Returns: Normalized popularity score (0-1) (float)
        return self.cluster_popularity.get(cluster_id, 0.5)

    # Get all recipes belonging to a specific cluster.
    def get_recipes_in_cluster(self, cluster_id):
        # Parameters:
        # cluster_id : The cluster ID (int)
        # Returns: All recipes in this cluster (DataFrame)
        return self.recipes_df[self.recipes_df['cluster_id'] == cluster_id]

    # Get a summary of all clusters with example recipes.
    def get_cluster_summary(self):
        # Returns: Summary of each cluster (dict)
        # --> For understanding what each cluster represents.
        summary = {}

        for cluster_id in range(self.n_clusters):
            cluster_recipes = self.get_recipes_in_cluster(cluster_id)

            # Get top 3 recipes in this cluster by rating
            top_recipes = cluster_recipes.nlargest(3, 'rating')['recipe_name'].tolist()

            summary[cluster_id] = {
                'num_recipes': len(cluster_recipes),
                'avg_rating': cluster_recipes['rating'].mean(),
                'popularity_score': self.cluster_popularity[cluster_id],
                'example_recipes': top_recipes
            }

        return summary


# HELPER FUNCTIONS

def load_clusterer(db_path='data/recipes.db', n_clusters=5, csv_fallback='data/sample_recipes.csv'):
    try:
        # If the DB is missing but a CSV fallback exists, create the DB on the fly.
        if not os.path.exists(db_path) and csv_fallback and os.path.exists(csv_fallback):
            df = pd.read_csv(csv_fallback)
            with sqlite3.connect(db_path) as conn:
                df.to_sql('recipes', conn, if_exists='replace', index=False)
            print(f"Created SQLite DB at {db_path} from CSV fallback {csv_fallback}")

        clusterer = RecipeClusterer(db_path, n_clusters)
        return clusterer
    except Exception as e:
        print(f"Error loading clusterer: {e}")
        return None
# Convenience function to load and initialize the clusterer.
    # Parameters:
    # db_path : Path to recipes SQLite DB file (str)
    # csv_fallback : Optional CSV path used to build the DB if missing (str)
    # n_clusters : Number of clusters to create (int)
    # Returns: Initialized and trained clusterer (RecipeClusterer)
    # Technical Note: We use this pattern to make the code cleaner and easier to use.


# TESTING CODE

if __name__ == "__main__":

    # Usage: python logic/clustering.py
   
    print("=" * 60)
    print("Testing Recipe Clustering Logic")
    print("=" * 60)
    print()

    # Test loading the clusterer
    clusterer = load_clusterer('../data/recipes.db', n_clusters=5, csv_fallback='../data/sample_recipes.csv')

    if clusterer:
        print("\n" + "=" * 60)
        print("Cluster Summary:")
        print("=" * 60)

        summary = clusterer.get_cluster_summary()
        for cluster_id, info in summary.items():
            print(f"\nCluster {cluster_id}:")
            print(f"  - Number of recipes: {info['num_recipes']}")
            print(f"  - Average rating: {info['avg_rating']:.2f}")
            print(f"  - Popularity score: {info['popularity_score']:.3f}")
            print(f"  - Example recipes: {', '.join(info['example_recipes'][:2])}")

        print("\n" + "=" * 60)
        print("Clustering logic test completed successfully!")
        print("=" * 60)
