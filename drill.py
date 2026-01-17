import streamlit as st
import requests

st.set_page_config(page_title="Pathfinder UK", page_icon="🔬")

st.title("🔬 Pathfinder: UKHSA Express")
st.write("Current Status: **Direct Satellite Uplink**")

# The Logic we discovered together
BASE_URL = "https://api.ukhsa-dashboard.data.gov.uk/themes/infectious_disease/"

if st.button("Initialize Deep Drill"):
    with st.spinner("Bypassing local restrictions..."):
        try:
            # Step 1: Get the sub-theme link from the list
            r = requests.get(BASE_URL, timeout=10)
            data = r.json()
            sub_themes_url = data[0]["sub_themes"]
            
            # Step 2: Hit the sub-themes endpoint
            r2 = requests.get(sub_themes_url, timeout=10)
            sub_themes = r2.json()
            
            st.success("✅ Connection Established. Clinical Categories mapped.")
            
            # Display them nicely in the UI
            for item in sub_themes:
                st.info(f"📂 Category: {item.get('name')}")
                
        except Exception as e:
            st.error(f"Logic Leak detected: {e}")