"""
COOKABLE - Recipe Clustering Logic
====================================

This module handles the machine learning aspect of the Cookable application.
It uses K-Means clustering to group similar recipes together based on their ingredients.

Technical Overview:
-------------------
This module implements how clustering works in practice.
K-Means is a simple, unsupervised machine learning algorithm that groups similar items together.

How it works:
-------------
1. Convert recipe ingredients into numerical vectors (feature extraction)
2. Apply K-Means clustering to group similar recipes
3. Calculate popularity scores for each cluster
4. Use these clusters to boost recommendations

Key Concepts:
-------------
- Feature Vector: A numerical representation of recipe ingredients
- Clustering: Grouping similar items together without labels
- K-Means: An algorithm that finds K groups (clusters) in the data
- Cluster Popularity: Average rating of all recipes in a cluster
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os


class RecipeClusterer:
    """
    This class handles recipe clustering using K-Means algorithm.

    Attributes:
    -----------
    recipes_df : DataFrame
        The loaded recipes dataset
    n_clusters : int
        Number of clusters to create (default: 5)
    kmeans_model : KMeans
        The trained K-Means model
    scaler : StandardScaler
        Scaler for normalizing features
    feature_vectors : ndarray
        Numerical representation of recipes
    cluster_popularity : dict
        Popularity score for each cluster
    """

    def __init__(self, csv_path, n_clusters=5):
        """
        Initialize the RecipeClusterer.

        Parameters:
        -----------
        csv_path : str
            Path to the recipes CSV file
        n_clusters : int
            Number of recipe clusters to create (default: 5)

        Technical Note:
        -----------------
        We use 5 clusters as a default because it provides a good balance:
        - Not too few (which would group very different recipes together)
        - Not too many (which would split similar recipes apart)
        """
        self.n_clusters = n_clusters
        self.recipes_df = None
        self.kmeans_model = None
        self.scaler = StandardScaler()
        self.feature_vectors = None
        self.cluster_popularity = {}

        # Load the recipes dataset
        self._load_recipes(csv_path)

        # Process ingredients and create feature vectors
        self._create_feature_vectors()

        # Train the clustering model
        self._train_clustering_model()

        # Calculate cluster-level popularity
        self._calculate_cluster_popularity()

    def _load_recipes(self, csv_path):
        """
        Load the recipes dataset from CSV.

        Technical Note:
        -----------------
        We use pandas to load CSV data because it provides powerful
        data manipulation capabilities and makes working with tabular data easy.
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Recipe dataset not found at: {csv_path}")

        # Load CSV into a pandas DataFrame
        self.recipes_df = pd.read_csv(csv_path)

        # Convert ingredients from string to list
        # CSV stores lists as strings like "Eggs,Milk,Flour"
        # We need to convert them to Python lists: ["Eggs", "Milk", "Flour"]
        self.recipes_df['ingredients'] = self.recipes_df['ingredients'].apply(
            lambda x: [ing.strip() for ing in x.split(',')]
        )

        print(f"✅ Loaded {len(self.recipes_df)} recipes from dataset")

    def _create_feature_vectors(self):
        """
        Convert recipe ingredients into numerical feature vectors.

        Technical Note:
        -----------------
        Machine learning algorithms work with numbers, not text.
        We need to convert ingredient lists into numerical vectors.

        Method: One-Hot Encoding
        ------------------------
        For each recipe, we create a binary vector where:
        - 1 means the ingredient is in the recipe
        - 0 means the ingredient is NOT in the recipe

        Example:
        Recipe: "Pasta Carbonara" = [Pasta, Eggs, Bacon, Parmesan]
        Vector: [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, ...]
                  ^^^^^^^^^^^^^^^    ^     ^           ^     ^
                  (other ingredients) Bacon Eggs       Parmesan Pasta

        This allows us to mathematically compare recipes!
        """

        # First, get a list of ALL unique ingredients across all recipes
        all_ingredients = set()
        for ingredients in self.recipes_df['ingredients']:
            all_ingredients.update(ingredients)

        # Sort for consistency
        all_ingredients = sorted(list(all_ingredients))
        print(f"📊 Found {len(all_ingredients)} unique ingredients")

        # Create feature vectors using one-hot encoding
        feature_vectors = []

        for ingredients in self.recipes_df['ingredients']:
            # Create a binary vector for this recipe
            vector = [1 if ing in ingredients else 0 for ing in all_ingredients]
            feature_vectors.append(vector)

        # Convert to numpy array for sklearn
        self.feature_vectors = np.array(feature_vectors)

        # Normalize the features using StandardScaler
        # This ensures all features have similar scales (mean=0, std=1)
        # Why? K-Means is sensitive to feature scales
        self.feature_vectors = self.scaler.fit_transform(self.feature_vectors)

        print(f"✅ Created feature vectors of shape: {self.feature_vectors.shape}")

    def _train_clustering_model(self):
        """
        Train the K-Means clustering model.

        Technical Note:
        -----------------
        K-Means Clustering Algorithm:
        1. Randomly place K cluster centers in the feature space
        2. Assign each recipe to the nearest cluster center
        3. Move each cluster center to the average position of its recipes
        4. Repeat steps 2-3 until cluster centers stop moving

        This creates K groups of similar recipes!

        Why K-Means?
        ------------
        - Simple and fast
        - Easy to understand
        - Works well for grouping similar items
        - Production-ready implementation
        """

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

        # Add cluster assignments to our DataFrame
        # Now each recipe knows which cluster it belongs to!
        self.recipes_df['cluster_id'] = self.kmeans_model.labels_

        print(f"✅ Trained K-Means model with {self.n_clusters} clusters")

        # Show how many recipes are in each cluster
        cluster_counts = self.recipes_df['cluster_id'].value_counts().sort_index()
        print("\n📊 Recipes per cluster:")
        for cluster_id, count in cluster_counts.items():
            print(f"   Cluster {cluster_id}: {count} recipes")

    def _calculate_cluster_popularity(self):
        """
        Calculate popularity score for each cluster.

        Technical Note:
        -----------------
        Cluster popularity is the average rating of all recipes in that cluster.
        If a cluster contains highly-rated recipes, it's a "popular" cluster.

        This helps us boost recommendations:
        - Recipes in popular clusters get a small bonus
        - This improves user satisfaction by recommending better-rated recipes

        Formula:
        --------
        cluster_popularity = mean(ratings of all recipes in cluster)

        We then normalize this to a 0-1 scale for easier combining with other scores.
        """

        # Calculate average rating per cluster
        for cluster_id in range(self.n_clusters):
            # Get all recipes in this cluster
            cluster_recipes = self.recipes_df[self.recipes_df['cluster_id'] == cluster_id]

            # Calculate average rating
            avg_rating = cluster_recipes['rating'].mean()

            # Store in our dictionary
            self.cluster_popularity[cluster_id] = avg_rating

        # Normalize to 0-1 scale
        # This makes it easier to combine with other scores later
        max_pop = max(self.cluster_popularity.values())
        min_pop = min(self.cluster_popularity.values())

        for cluster_id in self.cluster_popularity:
            if max_pop > min_pop:
                # Normalize: (value - min) / (max - min)
                normalized = (self.cluster_popularity[cluster_id] - min_pop) / (max_pop - min_pop)
                self.cluster_popularity[cluster_id] = normalized
            else:
                # If all clusters have same popularity, set to 0.5
                self.cluster_popularity[cluster_id] = 0.5

        print(f"\n✅ Calculated cluster popularity scores:")
        for cluster_id, pop in self.cluster_popularity.items():
            print(f"   Cluster {cluster_id}: {pop:.3f}")

    def get_recipe_cluster(self, recipe_name):
        """
        Get the cluster ID for a specific recipe.

        Parameters:
        -----------
        recipe_name : str
            Name of the recipe

        Returns:
        --------
        int or None
            Cluster ID if recipe found, None otherwise
        """
        recipe = self.recipes_df[self.recipes_df['recipe_name'] == recipe_name]
        if len(recipe) > 0:
            return int(recipe.iloc[0]['cluster_id'])
        return None

    def get_cluster_popularity(self, cluster_id):
        """
        Get the popularity score for a cluster.

        Parameters:
        -----------
        cluster_id : int
            The cluster ID

        Returns:
        --------
        float
            Normalized popularity score (0-1)
        """
        return self.cluster_popularity.get(cluster_id, 0.5)

    def get_recipes_in_cluster(self, cluster_id):
        """
        Get all recipes belonging to a specific cluster.

        Parameters:
        -----------
        cluster_id : int
            The cluster ID

        Returns:
        --------
        DataFrame
            All recipes in this cluster
        """
        return self.recipes_df[self.recipes_df['cluster_id'] == cluster_id]

    def get_cluster_summary(self):
        """
        Get a summary of all clusters with example recipes.

        Returns:
        --------
        dict
            Summary of each cluster

        Technical Note:
        -----------------
        This is useful for understanding what each cluster represents.
        For example:
        - Cluster 0 might be "pasta dishes"
        - Cluster 1 might be "breakfast items"
        - Cluster 2 might be "rice-based meals"
        """
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


# ========================================
# HELPER FUNCTIONS
# ========================================

def load_clusterer(csv_path='data/sample_recipes.csv', n_clusters=5):
    """
    Convenience function to load and initialize the clusterer.

    Parameters:
    -----------
    csv_path : str
        Path to recipes CSV file
    n_clusters : int
        Number of clusters to create

    Returns:
    --------
    RecipeClusterer
        Initialized and trained clusterer

    Technical Note:
    -----------------
    This is a "factory function" - it creates and returns an object.
    We use this pattern to make the code cleaner and easier to use.
    """
    try:
        clusterer = RecipeClusterer(csv_path, n_clusters)
        return clusterer
    except Exception as e:
        print(f"❌ Error loading clusterer: {e}")
        return None


# ========================================
# TESTING CODE (runs only if this file is executed directly)
# ========================================

if __name__ == "__main__":
    """
    This code runs only when you execute this file directly.
    It's useful for testing the clustering logic independently.

    Usage: python logic/clustering.py
    """
    print("=" * 60)
    print("Testing Recipe Clustering Logic")
    print("=" * 60)
    print()

    # Test loading the clusterer
    clusterer = load_clusterer('../data/sample_recipes.csv', n_clusters=5)

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
        print("✅ Clustering logic test completed successfully!")
        print("=" * 60)
