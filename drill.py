import streamlit as st
import requests
import json

st.set_page_config(page_title="Pathfinder UK", page_icon="🔬")

st.title("🔬 Pathfinder: UKHSA Express")
st.write("Status: **Global Inventory Mode**")

# This is the "Bedrock" URL - it rarely 404s because it's the root of the data
GLOBAL_URL = "https://api.ukhsa-dashboard.data.gov.uk/themes/"

def global_drill():
    try:
        r = requests.get(GLOBAL_URL, timeout=10)
        if r.status_code == 200:
            data = r.json()
            st.success("✅ Bedrock reached. Analyzing Global Themes...")
            
            # Show the raw map so we can see the NEW names
            for theme in data:
                theme_name = theme.get('name')
                # In the new API, the link IS the path
                link = theme.get('link')
                st.info(f"📍 **Theme:** {theme_name}")
                st.caption(f"Direct Path: {link}")
                
                # Let's try to peek inside one level automatically
                if theme_name == 'infectious_disease':
                    st.write("---")
                    st.write("🔍 Automatically scanning Infectious Disease structure...")
                    inner_r = requests.get(link)
                    st.json(inner_r.json()) # This will show us the EXACT new keys
        else:
            st.error(f"Global Handshake Failed: {r.status_code}")
    except Exception as e:
        st.error(f"Logic Leak: {e}")

if st.button("Run Global Discovery"):
    global_drill()
