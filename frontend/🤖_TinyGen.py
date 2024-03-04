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
st.sidebar.header("Additional Resources")
st.sidebar.page_link('https://tawsifkamal.notion.site/Tiny-Gen-3bc759c6254a4e33ad7f7fac86d97c0b?pvs=4)', label=":blue[Learn More About TinyGen]", icon = "🤔")
st.sidebar.page_link('https://github.com/tawsifkamal/TinyGen', label=':blue[GitHub]', icon='↗️')


st.title('🤖 TinyGen')

# Custom HTML to embed a YouTube video with specific aspect ratio
video_html = f"""
    <div style='position:relative; padding-bottom:56.25%; height:0; overflow:hidden;'>
        <iframe src='https://www.youtube.com/embed/aAXo5XXDPgE' frameborder='0' style='position:absolute; top:0; left:0; width:100%; height:100%;' allowfullscreen></iframe>
    </div>
"""

st.markdown(video_html, unsafe_allow_html=True)

st.write("""
TinyGen is an LLM Agent that is able to suggest :red[***code changes***] for you in a :red[***GitHub Repository***] of your choice!
         
Whether it's **feature additions**, or **fixing a bug**, or just giving you some guidance on how to implement something, TinyGen can assist you with your coding needs! Type in a **GitHub repo link** + **prompt** (or choose from a sample example below), and watch
the *magic* happen!

What is the *magic* you may ask? TinyGen will locate the :green[***exact code***] in the repository that addresses your prompt
and it will generate a :green[***unified diff***] showing the changes that need to be made.     
""")



def call_tiny_gen(repoUrl, prompt, model_name="TinyGen 1.0"):
    output_placeholder = st.empty()  # Create a placeholder for output
    full_output_text = ""  # Initialize an empty string to accumulate the output
    model_mapping = {"TinyGen 1.0": "tiny_gen_one", "TinyGen 2.0": "tiny_gen_two"}
    # Start the request
    with requests.post(f'{api_endpoint}{model_mapping[model_name]}/stream', json={"repoUrl": repoUrl, "prompt": prompt}, stream=True) as r:
        # Check the status code before proceeding
        if r.status_code == 200:
            with st.spinner(f'{model_name} doing its magic...'):
                for chunk in r.iter_content(chunk_size=100000):
                    chunk_text = chunk.decode('utf-8')
                    full_output_text += chunk_text  # Accumulate the chunk text
                    output_placeholder.text(full_output_text)  # Update the placeholder with the accumulated text
        else:
            # Handle errors for non-200 responses
            error_message = f"Failed to get a response from the server. Status code: {r.status_code}"
            st.error(error_message)
            return None  # Return None or an appropriate value indicating failure

    # If you reach this point, the response was successful and full_output_text contains your data
    return full_output_text
                    

# This function extracts the diff text after "Starting Reflection Chain..."
def extract_and_display_diff(full_output_text):
    reflection_chain_start = full_output_text.find("##### Starting Reflection Chain...")
    if reflection_chain_start != -1:  # Check if the section exists
        diff_text = full_output_text[reflection_chain_start:]
        diff_text = diff_text.split('\n', 1)[1] if '\n' in diff_text else diff_text
        st.markdown("#### Generated Diff:")
        st.markdown(diff_text)
    else:
        st.warning("Reflection Chain section not found in the response.")
 

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
        full_response_text = call_tiny_gen(repoUrl, prompt, chosen_model)
        extract_and_display_diff(full_response_text)
        st.toast("Diff Generated!", icon= "🎉")
    
    


    