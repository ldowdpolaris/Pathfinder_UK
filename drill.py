import streamlit as st
import requests
import json

st.set_page_config(page_title="Pathfinder UK", page_icon="🔬", layout="wide")

st.title("🔬 Pathfinder: UKHSA Express")

# The only hard link we need
BASE_URL = "https://api.ukhsa-dashboard.data.gov.uk/themes/infectious_disease/"

try:
    # 1. Get the Sub-Themes link
    r = requests.get(BASE_URL)
    data = r.json()
    
    # We check if it's a list (which we saw it was on your screen)
    if isinstance(data, list):
        sub_themes_url = data[0].get("sub_themes")
    else:
        sub_themes_url = data.get("sub_themes")

    if sub_themes_url:
        # 2. Get the actual list of categories
        res = requests.get(sub_themes_url)
        categories_data = res.json()
        
        # UI Setup
        st.subheader("Clinical Categories")
        
        # Handle if categories_data is a list of names or objects
        category_names = []
        for item in categories_data:
            if isinstance(item, dict):
                category_names.append(item.get("name"))
            else:
                category_names.append(item)

        selected_cat = st.selectbox("Choose a category:", category_names)

        if selected_cat:
            # 3. Construct the final Topic URL
            topic_url = f"{sub_themes_url}{selected_cat}/topics/"
            st.caption(f"Drilling: {topic_url}")
            
            t_res = requests.get(topic_url)
            if t_res.status_code == 200:
                topics = t_res.json()
                for t in topics:
                    st.success(f"🧪 **{t.get('name').replace('_', ' ').title()}**")
            else:
                st.warning("No topics found at this level yet.")
except Exception as e:
    st.error(f"Logic Leak: {e}")
    # This will show us the raw data so we can fix it if it fails again
    st.write("Raw Debug Data:", data)
