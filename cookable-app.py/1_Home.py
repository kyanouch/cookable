# COOKABLE - Main Landing Page
# This is the main entry point for the cookable web application.
# It contains the hero section, the concept explanation, some customer reviews, and the about section.


import streamlit as st

# ________________
# PAGE CONFIGURATION
# the following code snippet was added to make the app use full width of the window, as the default streamlit setting has margins.

st.set_page_config(
    page_title="COOKABLE - AI Recipe Matcher",
    layout="wide",
    page_icon="🍳",
    initial_sidebar_state="collapsed"  # Hide sidebar on landing page
)

#______________
# CUSTOM STYLING USING HTML and CSS
# To make our website look nicer, we used CSS to style some headings, the customer review carousel and buttons. 
# This section is heavily AI assisted as we do not know how to code in HTML and CSS. We understand that one uses HTML to arrange the elemetns and CSS to style them, so style="width: 100%; height: 200px" is CSS code inside HTML element.
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

#___________
# HERO SECTION
# Hero section - title and slogan. The first thing users see when they visit the app.
# Youtube tutorials recommended to use some images to make it more impactful, so we added Lottie files. 

# Using HTML and CSS again to style the main title. 
st.markdown(
    """
    <div style="width: 100%;">
        <div class="big-title">🍳 COOKABLE 🍳</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Adding some spacing with a blank empty string.
st.write("")


# SLOGAN WITH LOTTIE FILES
# Creating three columns to split the page and fit our lottie files with the slogan. 
col1, col2, col3 = st.columns([1, 2, 1])

# Left Lottie using HTML (again we used AI to help). 
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

# Slogan in the center
# Using HTML becasue we want to put the text nicely in a box. --> again AI assisted and suggested.  
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

# Right Lottie
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

# Horizontal line to separate the sections. 
st.markdown("---")

# ____________
# CONCEPT EXPLANATION
# To create a nicer user experience, we explain the concept and add some reviews. We got inspired by some startup landing pages and jargon. 
# We had fun with emojis once we learned that you can use them in Stremlit. They make the page look more colorful. 
st.write("#### 🍜 What is Cookable?")
st.write("Cookable is your go-to AI-Fridge. It suggests recipes based on what you have in the fridge.")
st.write("Stop wasting brain power on deciding what to cook - save it for university instead!")
st.write("")
st.write("")
st.write("#### 🥦 Why Cookable?")
st.write(
    "An average Cookable user saves up to 700 Hz of brain power daily - which they can direct into studying computer science instead."
)

st.markdown("---")

# ___________________
# CUSTOMER REVIEWS CAROUSEL
# This section is heavily AI assisted as we do not know how to create carousels using HTML.  
# This carousel automatically animates using CSS (-thanks AI!)
st.write("##### 🍗 What our users are saying:")

# Here are the quotes and authors.
quotes = [
    ("Cookable got dinner on the table in 10 minutes.", "BWL Justus"),
    ("Saved me when I had no idea what to cook with what I had.", "BWL Marie"),
    ("Finally stopped doom‑scrolling recipes.", "Thomas Bieger"),
    ("Takes whatever's in my fridge and makes it work.", "Erika the fly"),
]

# These are the cards from the carousel - using HTML and CSS for styling. 
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

# Duplicating the cards to create a loop effect. 
track_html = "".join(cards_html) * 2

# Rest of carousel animation - please ask codex for any additional questions. 
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

st.components.v1.html(carousel_html, height=360, scrolling=False)

st.markdown("---")

# __________________
# CALL TO ACTION
# This button to access the page where all the magic happens :)

st.write("### 👩‍🍳 Ready to find your next meal?")
st.write("Select the ingredients you have, and let your brain rest for a while.")

#Spacing
st.write("")

# Creating columns to center the button. 
# Button styling is already applied globally at the top of the page.
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Using the streamlit button funstion to switch pages. 
    if st.button("Start Cooking", use_container_width=True):
        st.switch_page("pages/2_Recipe_Finder.py")

st.markdown("---")

# _________________
# ABOUT SECTION
# I tried to imitate a startup story text (and make fun of it a bit). 
st.write("##### 🥸 About Cookable")
st.write("")

st.write(
    "Cookable was born from a simple observation: students waste too much time and brain power deciding what to cook. "
    "What started as a practical idea quickly turned into an obsession - we wanted to make students succeed by removing the everyday pain of starring at the fridge like it's an assessment math exam. "
    "The original goal was modest: build a smart app that helps people discover what they can cook based on the ingredients they already have. "
    "But somewhere between the first finished code snippets and the fiftieth error message, the idea took on a life of its own."
)

st.write("")

st.write(
    "Several weeks of intense development followed. There were moments of triumph when a feature finally worked, "
    "and moments of challenge when nothing made sense at 3 a.m. But the problem Cookable was trying to solve felt too real to ignore: "
    "people wasting time and mental energy simply because they didn't know what they could cook with what they had."
)

st.write("")

st.write(
    "What began as a simple idea slowly transformed into a real product with real users and real impact. "
    "Today, Cookable stands as a reminder that some of the best solutions don't begin with grand ambition—"
    "but with an empty fridge, a normal student at HSG, and a simple question: What can I cook right now?"
)

st.write("")
st.write("**Meet the team**") # --> https://github.com/adam-p/markdown-here/wiki/markdown-cheatsheet 
st.image(
    "https://github.com/kyanouch/cookable/blob/57dc2a9194420ee6fe992562d9124b4f1237064b/cookable-app.py/About_picture.png?raw=true",
    width=300
)

# Footer done with HTML and CSS again. Idea suggested in youtube videos. It was vibe coded with AI.
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; padding: 20px;'>"
    "Made with ❤️ for desperate HSG students | © 2025 Cookable"
    "</div>",
    unsafe_allow_html=True
)
