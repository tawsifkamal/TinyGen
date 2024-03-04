import streamlit as st
import requests
from ui_data import test_choices




#### FEEL FREE TO CHANGE THIS IF YOU WOULD LIKE TO TEST THE FAST API SERVER LOCALLY ($ uvicorn api.api:app --reload)
api_endpoint = "https://tiny-gen-zbkbev3qaq-uc.a.run.app/"
# api_endpoint = "http://localhost:8000/"


st.set_page_config(
    page_title="TinyGen",
    page_icon="🤖",
)

# Add a link to the sidebar
# Add a link to the sidebar
st.sidebar.header("Additional Resources")
st.sidebar.page_link('https://tawsifkamal.notion.site/Tiny-Gen-3bc759c6254a4e33ad7f7fac86d97c0b?pvs=4)', label=":blue[Learn More About TinyGen]", icon = "🤔")
st.sidebar.page_link('https://github.com/tawsifkamal/TinyGen', label=':blue[GitHub]', icon='↗️')


st.title('🕜 TinyGen: Non-Streaming')
st.write("""
TinyGen is an LLM Agent that is able to suggest :red[***code changes***] for you in a :red[***GitHub Repository***] of your choice!
         
Whether it's **feature additions**, or **fixing a bug**, or just giving you some guidance on how to implement something, TinyGen can assist you with your coding needs! Type in a **GitHub repo link** + **prompt** (or choose from a sample example below), and watch
the *magic* happen!

What is the *magic* you may ask? TinyGen will locate the :green[***exact code***] in the repository that addresses your prompt
and it will generate a :green[***unified diff***] showing the changes that need to be made.   

:red[***This page calls the NON STREAMING APIs***]. TinyGen takes time to respond. So, expect the runs to take around 1-2 minutes depending on the repo size!

""")
def call_tiny_gen(repoUrl, prompt, model_name = "TinyGen 1.0"):
    with st.spinner(f'Calling {model_name}... Please wait.'):
        if model_name == "TinyGen 1.0":
            res = requests.post(f"{api_endpoint}tiny_gen_one/call", json={"repoUrl": repoUrl, "prompt": prompt})
        else:
            res = requests.post(f"{api_endpoint}tiny_gen_two/call", json={"repoUrl": repoUrl, "prompt": prompt})

        # It's a good idea to check if the request was successful
    if res.status_code == 200:
        st.toast("Diff Generated!", icon="🎉")
        st.markdown("#### Generated Diff:")
        st.markdown(res.json())
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

if chosen_model == "TinyGen 1.0":
    extra_info = "*Works on **small** repos and on tasks that modify only **ONE** file*"
elif chosen_model == "TinyGen 2.0":
    extra_info = "*Works on **large or small** repos and on tasks that modify **one or MORE** files*"


st.write("**Chosen Model**: " + chosen_model + " ==> " + extra_info)


with st.form('my_form'):
    repoUrl = st.text_input('Enter the URL of the GitHub repository', repoUrl)
    prompt = st.text_area('Enter Prompt:', prompt, height=300) 
    submitted = st.form_submit_button('Submit')

    if submitted:
        call_tiny_gen(repoUrl, prompt, chosen_model)
    
    


    