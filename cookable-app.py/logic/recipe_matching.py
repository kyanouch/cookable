# Recipe Matching Logic
# This pages handles the core recipe matching algorithm.----------------

# This code builds a recommendation system that combines:
# 1. Rule-based filtering (ingredients matching)
# 2. Weighted factors scoring
# 3. Machine learning (clustering popularity)

# The Algorithm:
# 1. Filter recipes that can be made with available ingredients
# - Allow up to 2 missing ingredients (user can borrow from neighbor!)
# - Assume salt, pepper, oil, butter are always available
# 2. Calculate a base score for each recipe:
# - More matching ingredients = higher score
# - Fewer missing ingredients = higher score
# - Shorter cooking time = small bonus
# - Higher rating = higher score
# 3. Add ML boost from clustering:
# - Recipes in popular clusters get a bonus
# - Individual recipe rating also contributes
# 4. Rank recipes by final score and return top

import pandas as pd
import numpy as np

# Using object orientation 
class RecipeMatcher:
    # This class handles recipe matching and recommendation.
    # It takes user ingredients and finds the best matching recipes using a combination of rule-based filtering and scoring.

    def __init__(self, recipes_df, clusterer=None): # Initializing the RecipeMatcher.

        # Parameters:
        # - recipes_df : DataFrame - the recipes dataset
        # clusterer : RecipeClusterer, optional - the clustering model for ML boost
        # Technical Note:
        # We separate the matcher from the clusterer to follow "separation of concerns" - each class has one clear job.

        self.recipes_df = recipes_df.copy() # Making a copy of the incoming recipes DataFrame and keep it on the object, so changes inside the class don’t mutate the original DataFrame passed in.
        self.clusterer = clusterer 

        # Ingredients that are always assumed to be available
        # These are common pantry staples
        self.assumed_ingredients = {
            'Salt', 'Pepper', 'Oil', 'Butter',
            'Olive oil', 'Vegetable oil', 'Black pepper'
        }

        print(f"✅ Recipe Matcher initialized with {len(self.recipes_df)} recipes")

    def find_matching_recipes(self, user_ingredients, max_missing=2, top_n=5):
        """
        Find the best matching recipes for the user's ingredients.

        Parameters:
        -----------
        user_ingredients : list
            List of ingredients the user has
        max_missing : int
            Maximum number of missing ingredients allowed (default: 2)
        top_n : int
            Number of top recipes to return (default: 5)

        Returns:
        --------
        list of dict
            Top N matching recipes with scores and details

        Technical Note:
        -----------------
        This is the main algorithm that ties everything together!
        """

        # Convert user ingredients to a set for efficient operations
        # Sets allow us to use operations like intersection, difference, etc.
        user_ingredients_set = set(user_ingredients)

        # Add assumed ingredients to user's available ingredients
        user_ingredients_set.update(self.assumed_ingredients)

        print(f"\n🔍 Searching for recipes with {len(user_ingredients)} ingredients...")
        print(f"📋 User has: {', '.join(user_ingredients[:5])}{'...' if len(user_ingredients) > 5 else ''}")

        # List to store candidate recipes with their scores
        candidates = []

        # Iterate through all recipes
        for idx, recipe in self.recipes_df.iterrows():
            recipe_name = recipe['recipe_name']
            recipe_ingredients = set(recipe['ingredients'])
            recipe_rating = recipe['rating']
            cooking_time = recipe['cooking_time']

            # Calculate ingredient overlap
            # These are the ingredients the recipe needs that the user HAS
            matching_ingredients = user_ingredients_set.intersection(recipe_ingredients)

            # Calculate missing ingredients
            # These are the ingredients the recipe needs that the user DOESN'T have
            missing_ingredients = recipe_ingredients.difference(user_ingredients_set)

            num_matching = len(matching_ingredients)
            num_missing = len(missing_ingredients)
            num_total = len(recipe_ingredients)

            # ========================================
            # FILTERING: Only keep feasible recipes
            # ========================================
            # A recipe is feasible if it's missing at most max_missing ingredients
            if num_missing > max_missing:
                # Skip this recipe - too many missing ingredients
                continue

            # ========================================
            # BASE SCORE CALCULATION
            # ========================================
            # This is the non-ML part of the score
            base_score = self._calculate_base_score(
                num_matching=num_matching,
                num_missing=num_missing,
                num_total=num_total,
                cooking_time=cooking_time,
                rating=recipe_rating
            )

            # ========================================
            # ML BOOST: Cluster popularity
            # ========================================
            # If we have a clusterer, add cluster-based boost
            cluster_boost = 0.0
            cluster_id = None

            if self.clusterer:
                cluster_id = int(recipe['cluster_id'])
                cluster_popularity = self.clusterer.get_cluster_popularity(cluster_id)

                # Normalize recipe rating to 0-1 scale (assuming ratings are 1-5)
                normalized_rating = (recipe_rating - 1) / 4

                # Combine recipe popularity and cluster popularity
                # Weighted formula for ML boost calculation:
                # 0.2 * recipe_popularity + 0.2 * cluster_popularity
                cluster_boost = 0.2 * normalized_rating + 0.2 * cluster_popularity

            # ========================================
            # FINAL SCORE CALCULATION
            # ========================================
            # Combine base score (60%) with ML boost (40%)
            # Formula: 0.6 * base_score + 0.4 * cluster_boost
            final_score = 0.6 * base_score + 0.4 * cluster_boost

            # Store this candidate recipe
            candidates.append({
                'recipe_name': recipe_name,
                'final_score': final_score,
                'base_score': base_score,
                'cluster_boost': cluster_boost,
                'cluster_id': cluster_id,
                'matching_ingredients': list(matching_ingredients),
                'missing_ingredients': list(missing_ingredients),
                'num_matching': num_matching,
                'num_missing': num_missing,
                'rating': recipe_rating,
                'cooking_time': cooking_time,
                'difficulty': recipe['difficulty'],
                'instructions': recipe['instructions'],
                'all_ingredients': list(recipe_ingredients)
            })

        # ========================================
        # RANKING: Sort by final score
        # ========================================
        # Sort candidates by final score (highest first)
        candidates.sort(key=lambda x: x['final_score'], reverse=True)

        # Return top N recipes
        top_recipes = candidates[:top_n]

        print(f"✅ Found {len(candidates)} feasible recipes")
        print(f"🏆 Returning top {len(top_recipes)} recommendations")

        return top_recipes

    def _calculate_base_score(self, num_matching, num_missing, num_total,
                               cooking_time, rating):
        """
        Calculate the base score (non-ML part).

        Parameters:
        -----------
        num_matching : int
            Number of ingredients that match
        num_missing : int
            Number of missing ingredients
        num_total : int
            Total ingredients in recipe
        cooking_time : int
            Cooking time in minutes
        rating : float
            Recipe rating (1-5 stars)

        Returns:
        --------
        float
            Base score (0-1 range)

        Technical Note:
        -----------------
        This function uses a heuristic (rule of thumb) to score recipes.
        We combine multiple factors that we think make a recipe good:

        1. Ingredient Match Ratio (40% weight)
           - What % of recipe ingredients does the user have?
           - Higher is better

        2. Missing Ingredient Penalty (30% weight)
           - Fewer missing ingredients is better
           - We penalize each missing ingredient

        3. Cooking Time Factor (10% weight)
           - Shorter cooking time is slightly better
           - Busy people want quick meals!

        4. Rating Factor (20% weight)
           - Higher rated recipes are better
           - User satisfaction matters

        These weights are tunable - you can experiment with different values!
        """

        # ========================================
        # 1. INGREDIENT MATCH RATIO
        # ========================================
        # What percentage of the recipe's ingredients does the user have?
        # Example: Recipe needs 5 ingredients, user has 4 → match_ratio = 0.8
        if num_total > 0:
            match_ratio = num_matching / num_total
        else:
            match_ratio = 0.0

        # ========================================
        # 2. MISSING INGREDIENT PENALTY
        # ========================================
        # Penalize based on how many ingredients are missing
        # 0 missing = score 1.0, 1 missing = score 0.8, 2 missing = score 0.6
        if num_missing == 0:
            missing_penalty = 1.0
        elif num_missing == 1:
            missing_penalty = 0.8
        elif num_missing == 2:
            missing_penalty = 0.6
        else:
            missing_penalty = 0.0  # Too many missing (shouldn't reach here due to filtering)

        # ========================================
        # 3. COOKING TIME FACTOR
        # ========================================
        # Normalize cooking time to 0-1 scale
        # Shorter cooking time = higher score
        # We assume most recipes are 10-60 minutes
        # Time > 60 mins gets score near 0, Time < 10 mins gets score near 1
        max_time = 60  # minutes
        time_factor = max(0, 1 - (cooking_time / max_time))

        # ========================================
        # 4. RATING FACTOR
        # ========================================
        # Normalize rating to 0-1 scale (assuming ratings are 1-5)
        rating_factor = (rating - 1) / 4  # Maps [1,5] to [0,1]

        # ========================================
        # COMBINE ALL FACTORS WITH WEIGHTS
        # ========================================
        # These weights determine how important each factor is
        weight_match = 0.4  # 40% - Most important!
        weight_missing = 0.3  # 30% - Very important
        weight_time = 0.1  # 10% - Nice to have
        weight_rating = 0.2  # 20% - Quality matters

        base_score = (
            weight_match * match_ratio +
            weight_missing * missing_penalty +
            weight_time * time_factor +
            weight_rating * rating_factor
        )

        return base_score

    def get_recipe_details(self, recipe_name):
        """
        Get full details for a specific recipe.

        Parameters:
        -----------
        recipe_name : str
            Name of the recipe

        Returns:
        --------
        dict or None
            Recipe details if found, None otherwise
        """
        recipe = self.recipes_df[self.recipes_df['recipe_name'] == recipe_name]

        if len(recipe) > 0:
            recipe = recipe.iloc[0]
            return {
                'recipe_name': recipe['recipe_name'],
                'ingredients': recipe['ingredients'],
                'cooking_time': recipe['cooking_time'],
                'rating': recipe['rating'],
                'difficulty': recipe['difficulty'],
                'instructions': recipe['instructions']
            }
        return None


# ========================================
# HELPER FUNCTIONS
# ========================================

def create_matcher(recipes_df, clusterer=None):
    """
    Convenience function to create a RecipeMatcher.

    Parameters:
    -----------
    recipes_df : DataFrame
        Recipes dataset
    clusterer : RecipeClusterer, optional
        Clustering model

    Returns:
    --------
    RecipeMatcher
        Initialized matcher

    Technical Note:
    -----------------
    This is another factory function for cleaner code.
    """
    return RecipeMatcher(recipes_df, clusterer)


# ========================================
# TESTING CODE (runs only if this file is executed directly)
# ========================================

if __name__ == "__main__":
    """
    This code runs only when you execute this file directly.
    It's useful for testing the matching logic independently.

    Usage: python logic/recipe_matching.py
    """
    print("=" * 60)
    print("Testing Recipe Matching Logic")
    print("=" * 60)
    print()

    # Load recipes dataset
    import os
    csv_path = '../data/sample_recipes.csv'

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)

        # Convert ingredients from string to list
        df['ingredients'] = df['ingredients'].apply(
            lambda x: [ing.strip() for ing in x.split(',')]
        )

        # Add dummy cluster_id for testing without clusterer
        df['cluster_id'] = 0

        # Create matcher without clusterer
        matcher = create_matcher(df)

        # Test with sample ingredients
        test_ingredients = ['Eggs', 'Pasta', 'Bacon', 'Parmesan cheese']

        print(f"Testing with ingredients: {test_ingredients}\n")

        # Find matching recipes
        results = matcher.find_matching_recipes(
            user_ingredients=test_ingredients,
            max_missing=2,
            top_n=3
        )

        # Display results
        print("\n" + "=" * 60)
        print("Top Recommendations:")
        print("=" * 60)

        for i, recipe in enumerate(results, 1):
            print(f"\n{i}. {recipe['recipe_name']}")
            print(f"   ⭐ Rating: {recipe['rating']}/5")
            print(f"   ⏱️  Cooking time: {recipe['cooking_time']} mins")
            print(f"   🎯 Final score: {recipe['final_score']:.3f}")
            print(f"   ✅ Matching ingredients: {recipe['num_matching']}")
            print(f"   ❌ Missing ingredients: {recipe['num_missing']}")
            if recipe['num_missing'] > 0:
                print(f"      Missing: {', '.join(recipe['missing_ingredients'])}")

        print("\n" + "=" * 60)
        print("✅ Recipe matching test completed successfully!")
        print("=" * 60)
    else:
        print(f"❌ Recipe dataset not found at: {csv_path}")
        print("Make sure you're running from the project root directory")
