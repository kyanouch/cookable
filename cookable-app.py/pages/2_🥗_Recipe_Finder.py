# COOKABLE - Recipe Finder Page
# This page is the core interface for users of our project.  
# Users can select their available ingredients and see matching recipe recommendations
# The way it works:
# User selects ingredients from checkboxes with emoji indicators
# Selected ingredients are stored in session state
# User clicks "Find My Recipes" button to start the search
# Results appear directly on the same page below the ingredient selection
# The user can modify their selections and search again for updated results

# SESSION STATE EXPLANTION: 
# We got recommended (by AI) to use the function 'session state' of streamlit because our webiste is interactive.
# In order to keep the selected elements after reruning the app when the user clicks on the find recipes button. Without it a rerun will use the selection. 
# Information point (this is a pain to understand): https://youtu.be/92jUAXBmZyU?si=dZTb0-M9jz46sW7I https://youtu.be/5l9COMQ3acc?si=hy9EM9e0f2ihkIj8 

#_____________
# IMPORTS
import streamlit as st
import os
import sys
# These two imports allow us to import our logic modules (the backend of the app). These are two built-in Python modules that help navigate file paths and system paths inside our app. 

# This line tells Python to look the upper folder in the folder hierarchy. So we can import from the logic folder. 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Our machine learning 
from logic.clustering import load_clusterer
# The recipe matching system
from logic.recipe_matching import create_matcher

#_________________
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Recipe Finder - COOKABLE",
    layout="wide",
    page_icon="🥗"
)

# __________________
# CUSTOMIZING THE PAGE STYLE
st.markdown(
    """
    <style>
        .big-title {
            font-size: clamp(36px, 6vw, 64px);
            font-weight: 800;
            text-align: center;
            margin: 0;
            color: #15616D;
        }

        .ingredient-box {
            background: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
        }

        .recipe-card {
            background: #f9f9f9;
            border: 2px solid #15616D;
            border-radius: 12px;
            padding: 20px;
            margin: 16px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        /* Consistent button styling across the entire app */
        div.stButton > button {
            background-color: #15616D !important;
            color: white !important;
            font-size: 20px !important;
            padding: 14px 32px !important;
            border-radius: 12px !important;
            border: none !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
            transition: all 0.3s ease !important;
        }

        div.stButton > button:hover {
            background-color: #0d3d45 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 8px rgba(0,0,0,0.3) !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# _______________
# PAGE HEADER
# using HTML to create a big title with an emoji. Each time something is written in HTML or CSS, it's AI generated. 
# We did quite some vibe coding to make the page look good as the default streamlit style felt limited. 
st.markdown(
    """
    <div class="big-title">🥗 What's in Your Fridge?</div>
    """,
    unsafe_allow_html=True
)

st.write("")
st.write("#### Select all the ingredients you currently have available:")
st.write("")

# _______________
# INGREDIENT LIST WITH EMOJIS
# We created this list by asking for the most common ingredients in recipes. 
ingredients_list = [
    ("Eggs", "🥚"),
    ("Flour", "🌾"),
    ("Garlic", "🧄"),
    ("Onion", "🧅"),
    ("Milk", "🥛"),
    ("Tomatoes", "🍅"),
    ("Parmesan cheese", "🧀"),
    ("Feta cheese", "🧀"),
    ("Mozzarella cheese", "🧀"),
    ("Chicken", "🍗"),
    ("Soy sauce", "🥫"),
    ("Lemon", "🍋"),
    ("Carrots", "🥕"),
    ("Potatoes", "🥔"),
    ("Bell peppers", "🫑"),
    ("Rice", "🍚"),
    ("Beef", "🥩"),
    ("Pasta", "🍝"),
    ("Heavy cream", "🥛"),
    ("Broccoli", "🥦"),
    ("Mushrooms", "🍄"),
    ("Apples", "🍎"),
    ("Spinach", "🥬"),
    ("Banana", "🍌"),
    ("Bacon", "🥓"),
]

# ___________________
# SESSION STATE INITIALIZATION
# Initializing the session state variables to store what the user has selected. 
if "selected_ingredients" not in st.session_state:
    st.session_state.selected_ingredients = []
# if there is not prior selected ingredients, we created as an empty list.
if "show_results" not in st.session_state:
    st.session_state.show_results = False
# If there is ne show results variable in the session state, we created it ans set to false, so it doesn't show results yet. 

# ________________
# INGREDIENT SELECTION UI
st.write("---")

# Create a container for better organization
with st.container():
    # We'll display checkboxes in 3 columns for better space utilization
    col1, col2, col3 = st.columns(3)

    # Divide ingredients into 3 groups for the 3 columns
    total_ingredients = len(ingredients_list)
    per_column = (total_ingredients + 2) // 3  # Divide evenly with rounding up

    # Track which ingredients are selected
    selected = []

    # Column 1
    with col1:
        for i in range(0, per_column):
            if i < len(ingredients_list):
                ingredient, emoji = ingredients_list[i]
                if st.checkbox(f"{emoji} {ingredient}", key=f"ing_{i}"):
                    selected.append(ingredient)

    # Column 2
    with col2:
        for i in range(per_column, per_column * 2):
            if i < len(ingredients_list):
                ingredient, emoji = ingredients_list[i]
                if st.checkbox(f"{emoji} {ingredient}", key=f"ing_{i}"):
                    selected.append(ingredient)

    # Column 3
    with col3:
        for i in range(per_column * 2, total_ingredients):
            if i < len(ingredients_list):
                ingredient, emoji = ingredients_list[i]
                if st.checkbox(f"{emoji} {ingredient}", key=f"ing_{i}"):
                    selected.append(ingredient)

st.write("---")

# ========================================
# SELECTED INGREDIENTS SUMMARY
# ========================================
st.write("### 📋 Your Selected Ingredients:")

if selected:
    # Update session state with current selection
    st.session_state.selected_ingredients = selected

    # Display in a nice formatted way
    st.success(f"✅ You have selected **{len(selected)}** ingredient(s):")
    st.write(", ".join(selected))
else:
    # No ingredients selected yet
    st.info("👆 Check the boxes above to select your ingredients")
    st.session_state.selected_ingredients = []

st.write("")

# ========================================
# FIND RECIPES BUTTON
# ========================================
st.write("### 🎯 Ready to find recipes?")

if len(selected) > 0:
    st.write(f"Great! We'll find the best recipes based on your {len(selected)} ingredient(s).")

    # Create a centered button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Use Streamlit button which properly handles session state
        if st.button("🔍 Find My Recipes", use_container_width=True):
            # Set flag to show results below
            st.session_state.show_results = True
            # Force a rerun to display results
            st.rerun()
else:
    st.warning("⚠️ Please select at least one ingredient to continue")
    st.session_state.show_results = False

# ========================================
# HELPFUL TIPS SECTION
# ========================================
st.write("---")
st.write("### 💡 Tips:")
st.write("- **Salt, pepper, oil, and butter** are assumed to be available in unlimited amounts")
st.write("- We don't worry about exact quantities - just what you have!")
st.write("- Select all ingredients you have available, even if you're not sure you'll use them")
st.write("- If a recipe needs 1-2 extra ingredients, we'll let you know (time to visit your neighbor! 😉)")

# ========================================
# RECIPE RESULTS SECTION
# ========================================
# This section only appears after the user clicks "Find My Recipes"

if st.session_state.show_results and len(st.session_state.selected_ingredients) > 0:

    st.write("---")

    # ========================================
    # RESULTS HEADER
    # ========================================
    st.markdown(
        """
        <div class="big-title">🍽️ Your Perfect Recipes</div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    user_ingredients = st.session_state.selected_ingredients
    st.success(f"✅ Searching with **{len(user_ingredients)}** ingredient(s)")
    st.write("**Your ingredients:**", ", ".join(user_ingredients))
    st.write("---")

    # ========================================
    # LOAD DATA AND INITIALIZE MODELS
    # ========================================

    @st.cache_resource
    def initialize_models():
        """
        Initialize the clustering model and recipe matcher.

        Technical Note:
        -----------------
        We use @st.cache_resource decorator to cache this function.
        This means the models are loaded only ONCE and reused for all users.
        This improves performance and saves computation time!

        Returns:
        --------
        tuple
            (clusterer, recipes_df) or (None, None) if error
        """
        try:
            # Get the path to the CSV file
            csv_path = os.path.join('data', 'sample_recipes.csv')

            # If file doesn't exist, try absolute path
            if not os.path.exists(csv_path):
                csv_path = os.path.join(
                    os.getcwd(),
                    'data',
                    'sample_recipes.csv'
                )

            # Load and train the clustering model
            print("Loading clustering model...")
            clusterer = load_clusterer(csv_path, n_clusters=5)

            if clusterer is None:
                return None, None

            # Get the recipes DataFrame with cluster assignments
            recipes_df = clusterer.recipes_df

            print(f"✅ Models initialized successfully!")
            return clusterer, recipes_df

        except Exception as e:
            print(f"❌ Error initializing models: {e}")
            return None, None

    # Show loading message while models initialize
    with st.spinner("🔄 Loading recipe database and AI models..."):
        clusterer, recipes_df = initialize_models()

    # Check if models loaded successfully
    if clusterer is None or recipes_df is None:
        st.error("❌ Error loading recipe database. Please check the data file.")
    else:
        # ========================================
        # FIND MATCHING RECIPES
        # ========================================

        st.write("### 🔍 Finding Your Perfect Recipes...")

        # Create the recipe matcher with our clusterer
        matcher = create_matcher(recipes_df, clusterer)

        # Find matching recipes
        # Allow up to 2 missing ingredients, return top 5 recipes
        matching_recipes = matcher.find_matching_recipes(
            user_ingredients=user_ingredients,
            max_missing=2,
            top_n=5
        )

        st.write("---")

        # ========================================
        # DISPLAY RESULTS
        # ========================================

        if len(matching_recipes) == 0:
            # No recipes found
            st.warning("😕 We couldn't find any recipes matching your ingredients.")
            st.write("Try adding more ingredients or removing some restrictions.")

        else:
            # Recipes found!
            st.write(f"### 🎉 We Found {len(matching_recipes)} Amazing Recipes for You!")
            st.write("")

            # Display each recipe in an expandable card
            for idx, recipe in enumerate(matching_recipes, 1):
                # Recipe header with rank
                st.markdown(f"### {idx}. {recipe['recipe_name']}")

                # Create columns for recipe info
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("⭐ Rating", f"{recipe['rating']}/5")

                with col2:
                    st.metric("⏱️ Time", f"{recipe['cooking_time']} min")

                with col3:
                    st.metric("✅ Match", f"{recipe['num_matching']} ing.")

                with col4:
                    difficulty_emoji = {"easy": "😊", "medium": "😐", "hard": "😰"}
                    emoji = difficulty_emoji.get(recipe['difficulty'].lower(), "😊")
                    st.metric("🎯 Difficulty", f"{emoji} {recipe['difficulty'].title()}")

                # Show match score with color coding
                score_color = "#4CAF50" if recipe['final_score'] > 0.7 else "#FF9800"
                st.markdown(
                    f"<div style='background: {score_color}; color: white; padding: 8px; "
                    f"border-radius: 6px; text-align: center; font-weight: 600; margin: 8px 0;'>"
                    f"Match Score: {recipe['final_score']:.1%} | "
                    f"Base Score: {recipe['base_score']:.1%} | "
                    f"ML Boost: {recipe['cluster_boost']:.1%}"
                    f"</div>",
                    unsafe_allow_html=True
                )

                # Show missing ingredients if any
                if recipe['num_missing'] > 0:
                    missing = recipe['missing_ingredients']
                    st.warning(
                        f"⚠️ Missing {recipe['num_missing']} ingredient(s): "
                        f"**{', '.join(missing)}**\n\n"
                        f"💡 Time to visit your neighbor! 😉"
                    )

                # Expandable section for full recipe details
                with st.expander(f"📖 View Full Recipe: {recipe['recipe_name']}"):
                    st.write("#### Ingredients Needed:")
                    st.write("")

                    # Show all ingredients with checkmarks for what user has
                    for ingredient in recipe['all_ingredients']:
                        if ingredient in recipe['matching_ingredients']:
                            st.write(f"✅ {ingredient} *(you have this)*")
                        else:
                            st.write(f"❌ {ingredient} *(need to get this)*")

                    st.write("")
                    st.write("#### Instructions:")
                    st.write(recipe['instructions'])

                    st.write("")
                    st.write("#### Recipe Metadata:")
                    st.write(f"- **Cooking Time:** {recipe['cooking_time']} minutes")
                    st.write(f"- **Difficulty:** {recipe['difficulty'].title()}")
                    st.write(f"- **Rating:** {recipe['rating']}/5 stars")
                    if recipe['cluster_id'] is not None:
                        st.write(f"- **Recipe Cluster:** {recipe['cluster_id']} (similar recipes grouped by AI)")

                st.write("---")

        # ========================================
        # EDUCATIONAL SECTION: HOW IT WORKS
        # ========================================
        st.write("### 🎓 How Does This Work?")

        with st.expander("📚 Learn About Our Algorithm"):
            st.write("#### The Cookable Recipe Matching Algorithm")
            st.write("")

            st.write("""
            Our recommendation system combines **rule-based filtering** with **machine learning** to find the best recipes for you.
            Here's how it works step by step:
            """)

            st.write("#### Step 1: Filtering 🔍")
            st.write("""
            - We first filter recipes that you can **actually make** with your ingredients
            - We allow up to **2 missing ingredients** (you can borrow from a neighbor!)
            - We assume **salt, pepper, oil, and butter** are always available
            """)

            st.write("#### Step 2: Base Scoring 📊")
            st.write("""
            For each feasible recipe, we calculate a base score using:

            1. **Ingredient Match Ratio (40% weight)**
               - What percentage of the recipe's ingredients do you have?
               - Higher is better!

            2. **Missing Ingredient Penalty (30% weight)**
               - Fewer missing ingredients = higher score
               - 0 missing → full score, 1-2 missing → reduced score

            3. **Cooking Time Factor (10% weight)**
               - Shorter cooking time = small bonus
               - Busy people want quick meals!

            4. **Recipe Rating (20% weight)**
               - Higher rated recipes get a boost
               - Quality matters!
            """)

            st.write("#### Step 3: Machine Learning Boost 🤖")
            st.write("""
            We use **K-Means clustering** (unsupervised machine learning) to group similar recipes together.

            - Recipes are grouped into **5 clusters** based on their ingredients
            - Each cluster gets a **popularity score** (average rating of all recipes in that cluster)
            - Recipes in popular clusters get a **bonus boost**

            **Why clustering helps:**
            - If you like pasta dishes, we recommend other pasta dishes from the same cluster
            - Popular recipe types get prioritized
            - This improves user satisfaction!
            """)

            st.write("#### Step 4: Final Score 🎯")
            st.write("""
            We combine everything into a final score:

            ```
            Final Score = 0.6 × Base Score + 0.4 × ML Boost

            where:
            ML Boost = 0.2 × Recipe Rating + 0.2 × Cluster Popularity
            ```

            The recipes are then **ranked by final score**, and the top 5 are shown to you!
            """)

            st.write("")
            st.info("""
            💡 **Pro Tip:**

            This is a powerful recommendation system used in production!
            Real-world systems (like Netflix, Spotify) use more complex algorithms,
            but the core principles are the same:
            - Filtering
            - Scoring multiple factors
            - Combining with ML
            - Ranking results
            """)

        # ========================================
        # CLUSTERING INSIGHTS
        # ========================================
        st.write("### 🔬 Recipe Clustering Insights")

        with st.expander("🤖 View Clustering Analysis"):
            st.write("""
            Our AI has automatically grouped all recipes into **5 clusters** based on their ingredients.
            Recipes in the same cluster have similar ingredients and cooking styles.
            """)

            st.write("")
            st.write("#### Cluster Summary:")

            # Get cluster summary from clusterer
            cluster_summary = clusterer.get_cluster_summary()

            for cluster_id, info in cluster_summary.items():
                st.write(f"**Cluster {cluster_id}:**")
                st.write(f"- Number of recipes: {info['num_recipes']}")
                st.write(f"- Average rating: {info['avg_rating']:.2f}/5")
                st.write(f"- Popularity score: {info['popularity_score']:.2%}")
                st.write(f"- Example recipes: {', '.join(info['example_recipes'][:2])}")
                st.write("")

            st.write("")
            st.info("""
            💡 **How to read this:**
            - Higher **popularity score** means the cluster contains highly-rated recipes
            - Recipes in popular clusters get a **small boost** in recommendations
            - This helps us recommend tried-and-true recipe styles!
            """)

    # ========================================
    # MODIFY SEARCH SECTION
    # ========================================
    st.write("---")
    st.write("### 🔄 Want to try different ingredients?")
    st.write("Simply change your ingredient selections above and click 'Find My Recipes' again!")

    # Button to scroll back to top
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("1_🏠_Home.py")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; padding: 20px;'>"
    "Made with ❤️ for home cooks everywhere | © 2025 Cookable"
    "</div>",
    unsafe_allow_html=True
)
