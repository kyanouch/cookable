# 🍳 COOKABLE - AI-Powered Recipe Matcher

**A smart web application that recommends recipes based on the ingredients you have available.**

Never waste food again. Cookable uses AI and machine learning to match your available ingredients with delicious recipes.

---

## 📋 Overview

**Cookable** is a web application that helps you discover what you can cook with the ingredients in your fridge. The app combines intelligent filtering with K-Means clustering (machine learning) to provide personalized recipe recommendations.

### Key Features

- 🥗 **Ingredient Selection**: Choose from 23 common ingredients with visual icons
- 🤖 **Smart Matching**: AI algorithm finds recipes you can make (allowing up to 2 missing ingredients)
- 📊 **ML-Enhanced**: K-Means clustering groups similar recipes and recommends popular dishes
- 🎨 **Clean Interface**: Simple, intuitive design built with Streamlit
- ⚡ **Instant Results**: Get recipe recommendations on the same page without navigation
- 🔄 **Dynamic Updates**: Modify ingredients and refresh results instantly

---

## 🏗️ Project Structure

```
cookable-app/
│
├── 1_🏠_Home.py                      # Main landing page
│
├── pages/                          # Multi-page app structure
│   └── 2_🥗_Recipe_Finder.py      # Ingredient selection + Recipe results
│
├── logic/                          # Backend logic
│   ├── clustering.py               # K-Means clustering
│   └── recipe_matching.py          # Recipe matching algorithm
│
├── data/                           # Data files
│   └── sample_recipes.csv          # Recipe dataset (25 recipes)
│
├── README.md                       # This file
├── pyproject.toml                  # Project configuration
└── uv.lock                         # Dependency lock file
```

---

## ⚙️ Technology Stack

- **Python 3.11+**: Programming language
- **Streamlit**: Web application framework
- **scikit-learn**: Machine learning (K-Means clustering)
- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **UV**: Modern Python package manager

---

## 🚀 Quick Start

### Prerequisites

You need **UV** (modern Python package manager) installed.

#### Install UV:

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Verify installation:**
```bash
uv --version
```

---

### Installation

1. **Navigate to project directory:**
```bash
cd cookable-app
```

2. **Install dependencies:**
```bash
uv sync
```

This automatically installs all required packages.

---

### Running the App

**Start the application:**
```bash
uv run streamlit run 1_🏠_Home.py
```

**Or use the quick start script:**
```bash
./start.sh
```

The app will open in your browser at:
```
http://localhost:8501
```

---

## 📖 How to Use

### Step 1: Navigate to Recipe Finder

1. Open the app in your browser
2. Click "🥘 Start Cooking" on the landing page
3. You'll be taken to the integrated Recipe Finder page

### Step 2: Select Ingredients & Find Recipes

1. Check the boxes for ingredients you have available
2. See your selected ingredients summarized below
3. Click "🔍 Find My Recipes" button
4. Results appear instantly on the same page below

### Step 3: Explore Recommendations

1. See your top 5 recipe recommendations with:
   - Match scores and ML boost indicators
   - Ratings, cooking time, and difficulty
   - Missing ingredients (if any)
2. Click on recipe expanders to view:
   - Complete ingredient list
   - Step-by-step cooking instructions
   - Recipe metadata and cluster information

### Step 4: Refine & Cook!

1. Modify your ingredient selections anytime
2. Click "Find My Recipes" again for updated results
3. Choose a recipe and start cooking!

---

## 🧠 How It Works

### The Algorithm

Cookable uses a sophisticated 3-stage recommendation system:

#### 1. Filtering Phase

- Filters recipes based on available ingredients
- Allows up to **2 missing ingredients**
- Assumes basic pantry items (salt, pepper, oil, butter) are always available

#### 2. Base Scoring (60% of final score)

Evaluates recipes using multiple factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| Ingredient Match | 40% | Percentage of recipe ingredients you have |
| Missing Penalty | 30% | Fewer missing ingredients = higher score |
| Cooking Time | 10% | Faster recipes get a bonus |
| Recipe Rating | 20% | Higher rated recipes score better |

#### 3. Machine Learning Boost (40% of final score)

- **K-Means Clustering**: Groups recipes into 5 clusters based on ingredients
- **Cluster Popularity**: Each cluster has a popularity score
- **Smart Boosting**: Recipes in popular clusters get recommended more

**Final Score Formula:**
```
Final Score = 0.6 × Base Score + 0.4 × ML Boost

where:
ML Boost = 0.2 × Recipe Rating + 0.2 × Cluster Popularity
```

Recipes are ranked by final score, and the top 5 are displayed!

---

## 📊 Dataset

### Recipe Data

The app includes **25 sample recipes** with:

- Recipe name
- Ingredients list
- Cooking time (minutes)
- User ratings (1-5 stars)
- Step-by-step instructions
- Difficulty level (easy/medium/hard)

### Adding More Recipes

To expand the recipe database:

1. Open `data/sample_recipes.csv`
2. Add new rows following the existing format
3. Save the file
4. Restart the app

**Note**: Keep ingredient names consistent with the 23 available options.

---

## 🔧 Customization

### Adjust Number of Recommendations

Edit `pages/2_🥗_Recipe_Finder.py`:
```python
matching_recipes = matcher.find_matching_recipes(
    user_ingredients=user_ingredients,
    max_missing=2,  # Change max missing ingredients
    top_n=5         # Change number of recommendations
)
```

### Change Number of Clusters

Edit `logic/clustering.py`:
```python
clusterer = RecipeClusterer(csv_path, n_clusters=5)  # Change cluster count
```

### Modify Scoring Weights

Edit `logic/recipe_matching.py` in the `_calculate_base_score` method:
```python
weight_match = 0.4    # Ingredient match ratio
weight_missing = 0.3  # Missing ingredient penalty
weight_time = 0.1     # Cooking time factor
weight_rating = 0.2   # Recipe rating
```

### Update Final Score Formula

Edit `logic/recipe_matching.py` in `find_matching_recipes`:
```python
final_score = 0.6 * base_score + 0.4 * cluster_boost  # Adjust weights
```

---

## 🐛 Troubleshooting

### UV Command Not Found

**Solution**: Make sure UV is installed:
```bash
uv --version
```

If not found, reinstall using the installation instructions above.

---

### ModuleNotFoundError

**Solution**: Install all dependencies:
```bash
uv sync
```

---

### CSV File Not Found

**Solution**: Make sure you're running from the project root:
```bash
cd cookable-app
uv run streamlit run 1_🏠_Home.py
```

---

### Port Already in Use

**Solution**: Specify a different port:
```bash
uv run streamlit run 1_🏠_Home.py --server.port 8502
```

---

## 📦 UV Commands Reference

### Essential Commands

```bash
# Install all dependencies
uv sync

# Add a new package
uv add <package-name>

# Remove a package
uv remove <package-name>

# Run the app
uv run streamlit run 1_🏠_Home.py

# Run any Python script
uv run python <script.py>

# Update dependencies
uv lock --upgrade

# Show installed packages
uv pip list
```

---

## 🎯 Key Features

### Smart Recommendations

- Matches recipes to your available ingredients
- Allows borrowing 1-2 items from neighbors
- Prioritizes highly-rated recipes
- Considers cooking time preferences

### Machine Learning

- K-Means clustering groups similar recipes
- Learns from recipe popularity
- Boosts recommendations intelligently
- Adapts to recipe ratings

### User-Friendly Interface

- Clean, modern design
- Mobile-responsive layout
- Integrated single-page experience
- Easy ingredient selection with instant results
- Detailed recipe information with expandable views

---

## 🚀 Future Enhancements

Potential features for future versions:

- **User Accounts**: Save favorite recipes and preferences
- **API Integration**: Connect to recipe databases (Spoonacular, Edamam)
- **Dietary Filters**: Vegan, vegetarian, gluten-free options
- **Shopping Lists**: Auto-generate lists for missing ingredients
- **Recipe Upload**: Allow users to add their own recipes
- **Advanced ML**: Use embeddings for semantic similarity
- **Nutrition Info**: Display calories and macros
- **Meal Planning**: Plan meals for the entire week

---

## 📝 Technical Details

### Algorithm Components

1. **Rule-Based Filtering**: Ensures feasibility
2. **Heuristic Scoring**: Multi-factor evaluation
3. **ML Enhancement**: Cluster-based boosting
4. **Intelligent Ranking**: Optimized recommendations

### Machine Learning

- **Algorithm**: K-Means clustering
- **Features**: One-hot encoded ingredients
- **Preprocessing**: StandardScaler normalization
- **Clusters**: 5 recipe groups
- **Metric**: Euclidean distance

---

## 🔒 Privacy

- No data collection
- Runs entirely locally
- No external API calls
- No user tracking

---

## 🙏 Support

For issues or questions:

1. Check the troubleshooting section above
2. Review code comments in Python files
3. Ensure all dependencies are installed
4. Verify you're using Python 3.11+

---

## 📄 License

This project is proprietary software.

---

## 🎉 Get Started

Ready to discover your next meal?

```bash
uv run streamlit run 1_🏠_Home.py
```

**Happy Cooking! 🍳🥘🍝**

---

*© 2025 Cookable - Smart Recipe Recommendations*
