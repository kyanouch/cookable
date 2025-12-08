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
# if there is no prior selected ingredients, we created an empty list.

if "show_results" not in st.session_state:
    st.session_state.show_results = False
# If there is no show results variable in the session state, we created it and set to false, so it doesn't show results yet. 

# ________________
# INGREDIENT SELECTION UI
st.write("---")

# Creating a container for better organization of the code --> keeps elements of a section together
# To loop through the ingredients that are displayed in three columns, we used arithmetics and per_column variable to divide and loop throuh ingredients correctly.
# This per_column system was suggested by the same software engineer friend that helped us the setup configuration.  
with st.container():
    # We display checkboxes in 3 columns for better layout
    col1, col2, col3 = st.columns(3)

    # Dividing ingredients into 3 groups for the 3 columns, using the Python floor division operator that gives back a whole number. 
    total_ingredients = len(ingredients_list)
    per_column = (total_ingredients + 2) // 3 
    # This last formula ensures we evenely distribute ingredients across columns. (the +2 ensures rounding up when not divisible by 3)

    # Tracking which ingredients are selected
    selected = []

    with col1:
        for i in range(0, per_column): # looping through the first column of ingredients
            if i < len(ingredients_list): # without this line python gives an error - it makes sure that the loop doesn't run out of range of the list
                ingredient, emoji = ingredients_list[i] # grabbing tuple of selected element
                if st.checkbox(f"{emoji} {ingredient}", key=f"ing_{i}"): #giving each checkbox a unique identifier so that the value is stored correctly in sessions state. 
                    selected.append(ingredient) # Adding selected ingredients to the list of selected ingredients. 

    with col2:
        for i in range(per_column, per_column * 2):
            if i < len(ingredients_list):
                ingredient, emoji = ingredients_list[i]
                if st.checkbox(f"{emoji} {ingredient}", key=f"ing_{i}"):
                    selected.append(ingredient)

    with col3:
        for i in range(per_column * 2, total_ingredients):
            if i < len(ingredients_list):
                ingredient, emoji = ingredients_list[i]
                if st.checkbox(f"{emoji} {ingredient}", key=f"ing_{i}"):
                    selected.append(ingredient)

st.write("---")

# ___________________
# SELECTED INGREDIENTS SUMMARY
st.write("### 📋 Your selected ingredients:")

# if ... else statement to show different messages to orient the user 
if selected:
    # Updating session state with current selection
    st.session_state.selected_ingredients = selected

    # Display in a nice formatted way - green message, showing number in bold using ** 
    st.success(f"✅ You have selected **{len(selected)}** ingredient(s):")
    st.write(", ".join(selected)) # used AI to find the way to display it with commas 
else:
    # No ingredients selected yet
    st.info("👆 Check the boxes above to select your ingredients")
    st.session_state.selected_ingredients = []
# https://cheat-sheet.streamlit.app/ --> helped us find the different messages 
st.write("")

# ________________
# FIND RECIPES BUTTON
# interaction with user to start the recipe search
# To find how to best guide a user through the website we used existing websites as templates and generated possible user - UI dialogs with AI (our own versions felt weird and not prefessional).
st.write("### 🤌 Ready to find recipes?")

if len(selected) > 0:
    st.write(f"Great! We'll find the best recipes based on your {len(selected)} ingredient(s).") # progressing with the user dialog and making sure ingreditents are selected. 

    # Creating a centered button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Using button which properly handles session state
        if st.button("🔍 Find My Recipes", use_container_width=True): #to stretch the button full width we use the boolean option use_container_width=True - AI made and suggested
            # Using booleans to control the button and show results thanks to session state 
            st.session_state.show_results = True
            # Rerun to display results
            st.rerun()
else:
    st.warning("Please select at least one ingredient to continue") # --> https://cheat-sheet.streamlit.app/
    st.session_state.show_results = False

st.write("---")

# _____________________
# FOR SIMPLICITY PURPOSES 
# We wanted to keep things a bit simpler for us, so we don't care about quantites, and we assume that the most basic ingredients are always available. 
st.write("### ❕ Notes:")
st.write("- Salt, pepper, oil, and butter are assumed to be available all the time.")
st.write("- We don't worry about exact quantities - just what you have!")

# __________________________
# RECIPE RESULTS SECTION
# This section only appears after the user clicks "Find My Recipes"
# We ensure this by checking the session state and that the number of ingredients is not zero.
if st.session_state.show_results and len(st.session_state.selected_ingredients) > 0:

    st.write("---")

    # _____________________
    # RESULTS HEADER
    # HTML - done with AI 
    st.markdown(
        """
        <div class="big-title">🍽️ Your Perfect Recipes</div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # Getting the user's selection from the session state.
    # Interaction with user - making it more user friendly and porfessional.
    user_ingredients = st.session_state.selected_ingredients
    st.success(f"✅ Searching with **{len(user_ingredients)}** ingredient(s)")
    st.write("---")

    # _____________________
    # LOAD DATA AND INITIALIZE MODELS 

    # Initializing model function
    def initialize_models():
        # tuple (clusterer, recipes_df) 
        # Get the path to the CSV file with recipe data 
        # relative and absolute paths are tried to make sure it works in different environmaents --> this a modification that the built-in AI suggested and implemented to make error handling more robust. 
        rel_path = os.path.join('data', 'sample_recipes.csv') # relative (a shorter adress starting from our current working directory to the current file's directory)
        abs_path = os.path.join(os.getcwd(), 'data', 'sample_recipes.csv') # absolute (full adress from the root of the file system)

        tried_paths = [rel_path, abs_path]
        csv_path = None

        for path in tried_paths:
            print(f"Trying recipe CSV path: {path}")
            if os.path.exists(path): # chekcing of the path exists
                csv_path = path
                break 

        if csv_path is None:
            st.error(
                f"Could not find 'sample_recipes.csv'.\n"
            )
            return None, None # returning a tuple with two None values (None value is Python's built-in "no value")
            # for this code snippet we got assistance from the built-in AI in Vs code that makes suggestions. 
            # Frankly I do not understand fully what it suggested, but I accepted the change as it says it will make error handling more robust. 

        # Load and train the clustering model
        print("Loading clustering model...")
        clusterer = load_clusterer(csv_path, n_clusters=5) # function that calls reads the recipes from the CSV and builds/returns a clustering model object configured for 5 clusters.  
        # variable clusterer will hold the returned model object

        if clusterer is None: # failure check
            return None, None

        # Get the recipes DataFrame with cluster assignments. 
        recipes_df = clusterer.recipes_df # variable that holds the recipes table - DataFrame

        return clusterer, recipes_df # returns statement with a tuple of two variables -- the clusterer and the recipes table


    # Loading models 
    clusterer, recipes_df = initialize_models() # python's tuple unpacking. https://www.youtube.com/watch?v=yT-wF9_88Nw 

    #____________________
    # FINDING MATCHING RECIPES
    if clusterer is not None and recipes_df is not None:
        st.write("### 🔍 Finding your recipes...")

        # Create the recipe matcher with our clusterer
        matcher = create_matcher(recipes_df, clusterer) # our object

        # Find matching recipes
        # Reminder: allows up to 2 missing ingredients, return top 5 recipes
        # Using the method defined in our logic file 
        matching_recipes = matcher.find_matching_recipes( 
            user_ingredients=user_ingredients, #list pulled from session state 
            max_missing=2,
            top_n=5
        )

        st.write("---")

        # __________________
        # RESULTS DISPLAY

        # This code snippet is the answer our website gives the user. 
        # To handle the problem of not finding any recipe for the user's selection, we have put it in an if---else statement. 
        if len(matching_recipes) == 0:
            st.warning("We couldn't find any recipes matching your ingredients.")
        else:
            st.write(f"### 🧑‍🍳 We found {len(matching_recipes)} recipes for you!") # using an f string to display how many recipes were found.

            # Displaying each recipe in an expander. 
            # Using Python dictionnary - recipe, with all the info about each recipe. 
            # The values below come from the logic document. Here we simply display them. 
            for idx, recipe in enumerate(matching_recipes, 1): # Loops over the list matching recipes and enumerates it giving the index and the recipe. 
                # Finction enumerate allows to right down the recipe and it's index (idx)
                # we state that we start to enumerate at 1, as default number for Python is 0, so the index of the best recipe comes out on position 1. 
                # Recipe header with rank
                st.markdown(f"### {idx}. {recipe['recipe_name']}") # Using properties of Python dictionaries to pull out the desired values. 

                # Creating columns for recipe info. Again displaying information using properties of Python dictonaries. 
                col1, col2, col3, col4 = st.columns(4) # displaying data using st-metric (https://cheat-sheet.streamlit.app/)

                with col1:
                    st.metric("⭐ Rating", f"{recipe['rating']}/5") 

                with col2:
                    st.metric("⏱️ Time", f"{recipe['cooking_time']} min")

                with col3:
                    st.metric("✅ Match", f"{recipe['num_matching']} ing.") 

                with col4:
                    st.metric("💪 Difficulty", recipe['difficulty'].title())

                # Show match score with color coding --> AI assisted - codex vibe coding
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
                        f"Missing {recipe['num_missing']} ingredient(s): "
                        f"**{', '.join(missing)}**\n\n"
                        f"Time to visit your neighbor! 😉"
                    )

                # Expanders to display the details on the recipe in case the user wants to cook it. 
                with st.expander(f"📖 Open full recipe: {recipe['recipe_name']}"):
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
                    st.write("#### Recipe info:")
                    st.write(f"- Cooking Time: {recipe['cooking_time']} minutes")
                    st.write(f"- Difficulty: {recipe['difficulty'].title()}")
                    st.write(f"- Rating: {recipe['rating']}/5 stars")

                st.write("---")

        # ____________________
        # EDUCATIONAL SECTION --> I really like expanders, it makes the website super interactive and professional, so I decided to put an expander explaining how it works. 
        # it also portays our plan, what we were pursuing when we finally understood what exactly we have to code. This plan was suggested to us by AI in long dialogs to find the best logic for the matching. 
        st.write("### 🥘 How did we cook this website?")

        with st.expander("Click if you want to learn more about the algorithm"):
            st.write("#### The Cookable Recipe Matching Algorithm")
            st.write("")
            st.write("""
            Our recommendation system combines explicit rules and machine learning to find the best recipes.
            Here's how it works:
            """)

            st.write("#### 🍒 Step 1: Filtering")
            st.write("""
            - We first filter recipes that you can actually make with your ingredients by allowing up to two missing ingredients. 
            - We assume that salt, pepper, oil, and butter are always available for simplification purposes. 
            """)

            st.write("#### 🍇 Step 2: Rules-based score")
            st.write("""

            1. Ingredient Match Ratio (40% weight)
               - The higher the percentage of ingredients that the user has - the better.

            2. Missing Ingredient Penalty (30% weight)
               - The fewer the number of missing ingredients - the better. 

            3. Cooking Time Factor (10% weight)
               - Shorter cooking time - small bonus.

            4. Recipe Rating (20% weight)
               - Higher rated recipes get a boost
               - Quality matters!
            """)

            st.write("#### 🍉 Step 3: Machine learning boost")
            st.write("""
            We use K-Means clustering to group similar recipes together.
            - Recipes are grouped into 5 clusters based on their ingredients
            - Each cluster gets a popularity score (average rating of all recipes in that cluster)
            - Recipes in popular clusters get a bonus boost
            """)

            st.write("#### 🍫 Step 4: Final score")
            st.write("""
            We combine everything into a final score:

            Final Score = 0.6 × Base Score + 0.4 × ML Boost

            where:
            ML Boost = 0.2 × Recipe Rating + 0.2 × Cluster Popularity

            """)

            st.write("")

    # __________________
    # TRY AGAIN 
    st.write("---")
    st.write("### 🔄 Want to try different ingredients?")
    st.write("Simply change your ingredient selections above and click 'Find My Recipes'!")

# Footer - again vibe coded with AI
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; padding: 20px;'>"
    "Made with ❤️ for desperate HSG students | © 2025 Cookable"
    "</div>",
    unsafe_allow_html=True
)

