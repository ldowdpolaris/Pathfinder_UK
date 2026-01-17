import streamlit as st
import requests
import json

st.set_page_config(page_title="Pathfinder UK", page_icon="🔬", layout="wide")

st.title("🔬 Pathfinder: UKHSA Express")
st.write("Status: **Cloud-Verified Pipeline Active**")

# The North Star URL
BASE_URL = "https://api.ukhsa-dashboard.data.gov.uk/themes/infectious_disease/"

def safe_drill():
    try:
        r = requests.get(BASE_URL, timeout=10)
        if r.status_code == 200:
            data = r.json()
            
            # The API returns a list [ {...} ]. We need the first item.
            if isinstance(data, list) and len(data) > 0:
                core_data = data[0]
                
                # Check what keys are actually here to avoid the KeyError
                st.write(f"📡 *System Check Keys: {list(core_data.keys())}*")
                
                # Get the link to sub-themes (using .get to avoid crashes)
                sub_themes_link = core_data.get("sub_themes")
                
                if sub_themes_link:
                    st.success("🔗 Found Clinical Path. Drilling now...")
                    res = requests.get(sub_themes_link)
                    sub_themes = res.json()
                    
                    for item in sub_themes:
                        name = item.get("name", "Unknown Category")
                        st.info(f"📂 Category: {name}")
                else:
                    st.error("Target key 'sub_themes' not found in API response.")
            else:
                st.error("API returned an empty or unexpected list format.")
        else:
            st.error(f"Handshake Failed. Status: {r.status_code}")
            
    except Exception as e:
        st.error(f"⚠️ Logic Leak Details: {e}")

if st.button("Initialize Deep Drill"):
    safe_drill()
