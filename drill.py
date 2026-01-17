import streamlit as st
import requests
import json

st.set_page_config(page_title="Pathfinder UK", page_icon="🔬", layout="wide")

st.title("🔬 Pathfinder: UKHSA Express")
st.write("Live Data Feed: **Infectious Disease Portal**")

# 1. Get the Sub-Themes link from the Theme page
@st.cache_data
def get_sub_themes():
    base_url = "https://api.ukhsa-dashboard.data.gov.uk/themes/infectious_disease/"
    r = requests.get(base_url)
    # Reaching into the list we see on your screen right now
    sub_themes_path = r.json()[0]["sub_themes"]
    return requests.get(sub_themes_path).json()

try:
    sub_themes = get_sub_themes()
    
    # Create a nice layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Clinical Categories")
        # Let the user pick a category
        category_names = [item["name"] for item in sub_themes]
        selected_cat = st.radio("Select a category to drill deep:", category_names)

    with col2:
        if selected_cat:
            st.subheader(f"Topics in {selected_cat.replace('_', ' ').title()}")
            
            # Construct the Topic URL based on the selection
            topic_url = f"https://api.ukhsa-dashboard.data.gov.uk/themes/infectious_disease/sub_themes/{selected_cat}/topics/"
            
            res = requests.get(topic_url)
            if res.status_code == 200:
                topics = res.json()
                for t in topics:
                    # Create a "Card" for each topic
                    with st.expander(f"🧪 {t['name'].replace('_', ' ').title()}"):
                        st.write(f"**Internal ID:** `{t['name']}`")
                        st.caption(f"Endpoint: {topic_url}")
            else:
                st.warning("No specific topics found for this category yet.")

except Exception as e:
    st.error(f"Logic Leak: {e}")
