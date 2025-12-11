Project Structure

cookable-app/
│
├── 1_Home.py                       # Landing page
├── pages/                       
│   └── 2_Recipe_Finder.py          # Ingredient selection + Recipe results
│
├── logic/                          # Backend
│   ├── clustering.py               # K-Means clustering
│   └── recipe_matching.py          # Recipe matching algorithm
│
├── data/                           # Data files
│   └── sample_recipes.csv          # Recipe dataset (25 recipes)
│
├── README.md                      
├── pyproject.toml                  # Project configuration
└── uv.lock                         # Dependency lock file
