import streamlit as st
import requests
from ui_data import test_choices

st.set_page_config(
    page_title="Tiny Gen",
    page_icon="🤖",
)

# Add a link to the sidebar
st.sidebar.markdown('[Learn More About Tiny Gen](https://tawsifkamal.notion.site/Tiny-Gen-3bc759c6254a4e33ad7f7fac86d97c0b?pvs=4)', unsafe_allow_html=True)


st.title('🤖 Tiny Gen')
st.write("""
TinyGen is an LLM Agent that is able to make code changes for you in any GitHub repository!
Simply type in a desired GitHub repository link and prompt (or choose from a sample project example from below), and watch
for the magic to happen!

What is the magic you may ask? TinyGen will locate the **exact code** in the repository that addresses the request made in the prompt
and it will generate a **unified diff** showing the changes that need to be made in order to fulfill the request.         

Currently, the model is a bit slow, so expect the runs to take around 1-2 minutes!

""")
def call_tiny_gen(repoUrl, prompt, model_name = "TinyGen 1.0"):
    with st.spinner(f'Calling {model_name}... Please wait.'):
        if model_name == "TinyGen 1.0":
            res = requests.post("https://tiny-gen-zbkbev3qaq-uc.a.run.app/tiny_gen_one/call", json={"repoUrl": repoUrl, "prompt": prompt})
        else:
            res = requests.post("https://tiny-gen-zbkbev3qaq-uc.a.run.app/tiny_gen_two/call", json={"repoUrl": repoUrl, "prompt": prompt})

        # It's a good idea to check if the request was successful
    if res.status_code == 200:
        st.info(res.json())
    else:
        st.error('Failed to get a response from the server.')


# Creating a mapping for options
option_names = [choice["name"] for choice in test_choices]
options_map = {choice["name"]: choice for choice in test_choices}

option = st.selectbox(
    '##### Try a sample Project',
    option_names)

# Use the selected option to get the prompt and repoUrl
selected_choice = options_map[option]
prompt = selected_choice["prompt"].strip()
repoUrl = selected_choice["repoUrl"].strip()

chosen_model = st.radio(
    "##### Pick your model",
    ["TinyGen 1.0", "TinyGen 2.0"],
    index=0,
)

st.write("**Chosen Model**: " + chosen_model)


with st.form('my_form'):
    repoUrl = st.text_input('Enter the URL of the GitHub repository', repoUrl)
    prompt = st.text_area('Enter Prompt:', prompt, height=300) 
    submitted = st.form_submit_button('Submit')

    if submitted:
        call_tiny_gen(repoUrl, prompt, chosen_model)
    
    


    