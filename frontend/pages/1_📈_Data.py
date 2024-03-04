import streamlit as st
import requests
import pandas as pd

# Set page config
st.set_page_config(page_title="Data", page_icon="📈")
# Add a link to the sidebar
st.sidebar.markdown('[Learn More About Tiny Gen](https://tawsifkamal.notion.site/Tiny-Gen-3bc759c6254a4e33ad7f7fac86d97c0b?pvs=4)', unsafe_allow_html=True)

# Main page title
st.title('📈 Tiny Gen Past Calls')
st.write("""
         This page shows all of the past calls to TinyGen 1.0 and TinyGen 2.0. Each time a model is invoked,
         the `repoUrl`, `prompt`, and `response` of the TinyGen are stored in a database for the corresponding model.
         This page calls the API endpoints that return all of the data.
         Below, you can inspect the data for all of the calls in a tabular format.
         """)


# Fetching data
data_url_1 = "https://tiny-gen-zbkbev3qaq-uc.a.run.app/tiny_gen_one/get_past_calls"
data_url_2 = "https://tiny-gen-zbkbev3qaq-uc.a.run.app/tiny_gen_two/get_past_calls"

try:
    response_1 = requests.get(data_url_1)
    response_1.raise_for_status()  # Raises a HTTPError if the response status code is 4XX/5XX
    data_1 = response_1.json()['data']

    response_2 = requests.get(data_url_2)
    response_2.raise_for_status()
    data_2 = response_2.json()['data']
    
except requests.exceptions.HTTPError as http_err:
    st.error(f"HTTP error occurred: {http_err}")
except Exception as err:
    st.error(f"An error occurred: {err}")
else:
    if data_1:
        st.subheader("TinyGen 1.0 Past Calls")
        df_1 = pd.DataFrame(data_1)
        st.dataframe(df_1)
    else:
        st.write("No data available for TinyGen 1.0")

    if data_2:
        st.subheader("TinyGen 2.0 Past Calls")
        df_2 = pd.DataFrame(data_2)
        st.dataframe(df_2)
    else:
        st.write("No data available for TinyGen 2.0")
