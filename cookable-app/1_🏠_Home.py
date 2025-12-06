"""
COOKABLE - Main Landing Page
=============================
This is the main entry point for the cookable web application.
It displays the hero section, concept explanation, customer reviews, and about section.

The app uses Streamlit's page navigation to allow users to navigate to the
Recipe Input page where they can select ingredients.
"""

import streamlit as st

# ========================================
# PAGE CONFIGURATION
# ========================================
# Set the page to use the full browser width instead of Streamlit's default centered layout
# This gives us more space for our content and makes the UI look more modern
st.set_page_config(
    page_title="COOKABLE - AI Recipe Matcher",
    layout="wide",
    page_icon="🍳",
    initial_sidebar_state="collapsed"  # Hide sidebar on landing page
)

# ========================================
# CUSTOM CSS STYLING
# ========================================
# We use custom CSS to create a more polished, professional look
# This includes large titles, styled boxes, responsive font sizes, and consistent button styling
st.markdown(
    """
    <style>
        /* Main title styling - uses clamp() for responsive sizing */
        .big-title {
            font-size: clamp(42px, 8vw, 96px);
            font-weight: 800;
            text-align: center;
            margin: 0;
            color: #15616D;
        }

        /* Subtitle styling */
        .big-sub {
            font-size: clamp(18px, 3vw, 28px);
            color: #555;
            text-align: center;
            margin: 6px 0 18px 0;
        }

        /* Boxed content styling - creates nice bordered sections */
        .boxed {
            border: 1px solid #d9d9d9;
            border-radius: 12px;
            padding: 18px 20px;
            background: #fff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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

# ========================================
# HERO SECTION
# ========================================
# The hero section is the first thing users see - it needs to be impactful
st.markdown(
    """
    <div style="width: 100%;">
        <div class="big-title">🍳 COOKABLE</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Add some vertical spacing
st.write("")

# ========================================
# MAIN SLOGAN / TAGLINE WITH LOTTIE ANIMATIONS
# ========================================
# We use a 3-column layout with Lottie animations on both sides of the slogan
# The Lottie files show food animations to make the page more engaging
col1, col2, col3 = st.columns([1, 2, 1])

# Left Lottie animation
with col1:
    st.components.v1.html(
        """
        <script
          src="https://unpkg.com/@lottiefiles/dotlottie-wc@0.8.5/dist/dotlottie-wc.js"
          type="module"
        ></script>

        <dotlottie-wc
          src="https://lottie.host/94c71d8d-2c77-4f1b-bee6-9136b9f38ec5/1YKowIe1na.lottie"
          style="width: 100%; height: 200px"
          autoplay
          loop
        ></dotlottie-wc>
        """,
        height=220,
    )

# Center slogan
with col2:
    st.markdown(
        """
        <div class='boxed' style='text-align:center;'>
            <h1 style='margin:0; font-size: 28px;'>
                Because googling 'chicken recipe' for the 47th time is exhausting.
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Right Lottie animation
with col3:
    st.components.v1.html(
        """
        <script
          src="https://unpkg.com/@lottiefiles/dotlottie-wc@0.8.5/dist/dotlottie-wc.js"
          type="module"
        ></script>

        <dotlottie-wc
          src="https://lottie.host/94c71d8d-2c77-4f1b-bee6-9136b9f38ec5/1YKowIe1na.lottie"
          style="width: 100%; height: 200px"
          autoplay
          loop
        ></dotlottie-wc>
        """,
        height=220,
    )

# Horizontal divider to separate sections
st.markdown("---")

# ========================================
# CONCEPT EXPLANATION
# ========================================
# This section explains what Cookable does and why it's useful
st.write("#### 🎯 What is Cookable?")
st.write(
    "Cookable is your go-to AI-Fridge. It suggests recipes based on what you have in the fridge. "
    "Stop wasting brain power on deciding what to eat every day."
)

st.write("")
st.write("")

st.write("#### 🧠 Why Cookable?")
st.write(
    "An average Cookable user saves up to 700 Hz of brain power daily, "
    "which they can direct into studying computer science instead."
)

st.markdown("---")

# ========================================
# CUSTOMER REVIEWS CAROUSEL
# ========================================
# This creates a horizontally scrolling carousel of customer testimonials
# The carousel automatically animates using CSS keyframes
st.write("##### 💬 What our users are saying:")

# Define customer quotes and their authors
quotes = [
    ("Cookable got dinner on the table in 10 minutes.", "Justus"),
    ("Saved me when I had no idea what to cook with what I had.", "Marie"),
    ("Finally stopped doom‑scrolling recipes.", "Thomas"),
    ("Takes whatever's in my fridge and makes it work.", "Erika"),
]

# Build HTML for each quote card with modern styling
cards_html = []
for text, author in quotes:
    cards_html.append(
        f"""
        <div class="testimonial-card">
            <div class="quote-icon">❝</div>
            <div class="stars">⭐⭐⭐⭐⭐</div>
            <p class="quote-text">{text}</p>
            <div class="author-section">
                <div class="avatar">{author[0]}</div>
                <p class="quote-author">{author}</p>
            </div>
        </div>
        """
    )

# Duplicate the cards to create seamless infinite scroll effect
track_html = "".join(cards_html) * 2

# Complete carousel HTML with modern CSS
carousel_html = f"""
<style>
    .carousel-shell {{
        overflow: hidden;
        width: 100%;
        padding: 32px 0;
        background: linear-gradient(to bottom, transparent, rgba(21, 97, 109, 0.03), transparent);
    }}

    .carousel-track {{
        display: flex;
        gap: 24px;
        animation: slide-left 40s linear infinite;
    }}

    .carousel-track:hover {{
        animation-play-state: paused;
    }}

    .testimonial-card {{
        flex: 0 0 380px;
        background: linear-gradient(135deg, #ffffff 0%, #f8feff 100%);
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 8px 24px rgba(21, 97, 109, 0.12);
        border: 1px solid rgba(21, 97, 109, 0.1);
        position: relative;
        transition: all 0.3s ease;
    }}

    .testimonial-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 12px 32px rgba(21, 97, 109, 0.18);
        border-color: rgba(21, 97, 109, 0.2);
    }}

    .quote-icon {{
        position: absolute;
        top: 16px;
        right: 20px;
        font-size: 48px;
        color: rgba(21, 97, 109, 0.1);
        font-family: Georgia, serif;
        line-height: 1;
    }}

    .stars {{
        font-size: 18px;
        margin-bottom: 12px;
        letter-spacing: 2px;
    }}

    .quote-text {{
        font-size: 17px;
        line-height: 1.7;
        color: #333;
        margin: 16px 0 20px 0;
        font-style: italic;
        min-height: 80px;
    }}

    .author-section {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: auto;
        padding-top: 16px;
        border-top: 1px solid rgba(21, 97, 109, 0.1);
    }}

    .avatar {{
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: linear-gradient(135deg, #15616D 0%, #1a7785 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(21, 97, 109, 0.2);
    }}

    .quote-author {{
        font-weight: 700;
        color: #15616D;
        font-size: 16px;
        margin: 0;
    }}

    /* Keyframe animation for sliding effect */
    @keyframes slide-left {{
        from {{ transform: translateX(0); }}
        to {{ transform: translateX(-50%); }}
    }}

    /* Responsive design for smaller screens */
    @media (max-width: 720px) {{
        .testimonial-card {{
            flex-basis: 320px;
            padding: 24px;
        }}

        .quote-text {{
            font-size: 16px;
            min-height: 70px;
        }}
    }}
</style>
<div class="carousel-shell">
    <div class="carousel-track">
        {track_html}
    </div>
</div>
"""

# Render the carousel using Streamlit's HTML component
st.components.v1.html(carousel_html, height=360, scrolling=False)

st.markdown("---")

# ========================================
# CALL TO ACTION
# ========================================
# This button encourages users to start using the app
#
# Technical Note:
# ---------------
# We use Streamlit's native navigation with custom CSS for beautiful styling
st.write("### 🚀 Ready to find your next meal?")
st.write("Select the ingredients you have, and let our AI recommend the perfect recipes for you!")

st.write("")

# Create centered button layout
# Button styling is already applied globally at the top of the page
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Use Streamlit's native button with custom styling
    if st.button("🥘 Start Cooking", use_container_width=True):
        st.switch_page("pages/2_🥗_Recipe_Finder.py")

st.markdown("---")

# ========================================
# ABOUT SECTION
# ========================================
# The story behind Cookable - makes it more personal and engaging
st.write("##### 📖 About Cookable")
st.write("")

st.write(
    "Cookable was born from a simple observation: people waste too much time deciding what to cook. "
    "What started as a practical idea quickly turned into an obsession. The original goal was modest: "
    "build a smart app that helps people discover what they can cook based on the ingredients they already have. "
    "But somewhere between the first prototype and the tenth bug that refused to die, the idea took on a life of its own."
)

st.write("")

st.write(
    "Several weeks of intense development followed. There were moments of triumph when a feature finally worked, "
    "and moments of challenge when nothing made sense at 3 a.m. The problem Cookable was trying to solve felt "
    "too real to ignore: people wasting time and mental energy simply because they didn't know what they could "
    "cook with what they had. Every iteration made the app smarter, faster, and more useful."
)

st.write("")

st.write(
    "What began as a simple idea slowly transformed into a real product with real users and real impact. "
    "Today, Cookable stands as a reminder that some of the best solutions don't begin with grand ambition—"
    "but with an empty fridge, a busy person, and a simple question: What can I cook right now?"
)

st.write("")
st.write("**Meet the team** 👨‍💻👩‍💻")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; padding: 20px;'>"
    "Made with ❤️ for home cooks everywhere | © 2025 Cookable"
    "</div>",
    unsafe_allow_html=True
)
