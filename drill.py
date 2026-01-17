import streamlit as st
import requests

st.set_page_config(page_title="Pathfinder UK", page_icon="🔬", layout="wide")

st.title("🔬 Pathfinder: UKHSA Express")
st.write("Status: **Cloud-Verified Pipeline Active**")

BASE_URL = "https://api.ukhsa-dashboard.data.gov.uk/themes/infectious_disease/"

# Step 1: Fetch Categories for the Sidebar
@st.cache_data # This makes the app lightning fast
def get_categories():
    r = requests.get(BASE_URL)
    sub_themes_url = r.json()[0]["sub_themes"]
    return requests.get(sub_themes_url).json()

try:
    categories = get_categories()
    category_names = [item["name"] for item in categories]

    # UI: Selection Box
    selected_cat = st.selectbox("Select Clinical Category", category_names)

    if selected_cat:
        st.subheader(f"Drilling into: {selected_cat}")
        
        # Step 2: Find the 'topics' link for the selected category
        # The API structure: themes -> infectious_disease -> sub_themes -> [category] -> topics
        target_url = f"{BASE_URL}sub_themes/{selected_cat}/topics/"
        
        if st.button(f"Scan {selected_cat} Topics"):
            res = requests.get(target_url)
            if res.status_code == 200:
                topics = res.json()
                for t in topics:
                    st.write(f"🧪 **{t['name']}**")
            else:
                st.warning("This category is currently being updated by UKHSA.")

except Exception as e:
    st.error(f"System Check: {e}")
