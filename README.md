
# Welcome To The TinyGen Repo!

### What is TinyGen?
[https://www.loom.com/share/fea73acba34948c09b7e7960dc1d1cd1](https://www.loom.com/share/547415955cb044e7b03edcd0cd00aa18?sid=fea94a6f-d0bf-4bdd-93cc-faf3cce1cf4f)

### Calling TinyGen Through The Production API
https://www.loom.com/share/81cad00f51b04b1ab823cb3f58fda866

## Useful Links

- [TinyGen UI](https://tiny-gen.streamlit.app/)
- [Production API Base Url](https://tiny-gen-zbkbev3qaq-uc.a.run.app)
- [Public Postman Collection To Interact With API](https://www.postman.com/red-water-664033/workspace/tinygen/documentation/17857495-f27f8dae-edd0-4a36-8382-809507a65587)
- [TinyGen Project Overview](https://tawsifkamal.notion.site/TinyGen-3bc759c6254a4e33ad7f7fac86d97c0b?pvs=74)
*Edit: Streaming is implemented! Use it through the Streamlit UI or find the endpoints on the API documentation page*
## Stack
- Python
- FastAPI
- Google Cloud Run (API Deployment)
- Streamlit & Streamlit Cloud (Frontend + Deployment)
- Supabase (LLM Call Storage)

## Development

1. Clone the project project to your computer

```
git clone https://github.com/tawsifkamal/TinyGen.git
```

2. Navigate to this project in your terminal

```
cd TinyGen
```

3. Obtain the secrets. Use your own or contact me!

If using your own, create a .env file and add the following api keys:

```
GITHUB_API_TOKEN=
SUPABASE_URL=
SUPABASE_KEY=
OPENAI_API_KEY=
```

- Github API is required to process all of the files from a given repository
- Supabase is used to store all of the prompts, repoUrls, and responses provided to TinyGen
- OpenAI is the provider for all models used for TinyGen (GPT-4 and GPT-3.5)

4. Install Virtualenv if not it does not exist on your local machine:

```
pip install virtualenv
```

5. Create a virtual environment
```
virtualenv venv
```


6. Activate the virtual environment

```
source venv/bin/activate
```

7. Install all necessary packages
```
pip install -r requirements.txt
```

8. Start the Fast API Server
```
uvicorn api.api:app --reload
```

9. Open another terminal and start the streamlit frontend
```
streamlit run frontend/🤖_TinyGen.py
```

I know it's a bit wierd to have a funky emoji for a file name. But that's how Streamlit chose to do its user design.🤷🏽‍♂️
Please let me know if you do have any problems with running the file!

# Making API Calls Directly
The following endpoints are available when making api calls. A public workspace on postman is linked [here](https://elements.getpostman.com/redirect?entityId=17857495-f27f8dae-edd0-4a36-8382-809507a65587&entityType=collection)

**Full link**

https://elements.getpostman.com/redirect?entityId=17857495-f27f8dae-edd0-4a36-8382-809507a65587&entityType=collection

Otherwise, feel free to call the APIs yourself using your preferred API client. The endpoints are listed below:

If using local API, base_url = ```http://localhost:8000```

If using prod API, base_url = ```https://tiny-gen-zbkbev3qaq-uc.a.run.app```

Tip! The docs for the API is located at the root endpoint ```/```
## Call TinyGen

**Call TinyGen 1.0**

```POST /tiny_gen_one/call``` 

- Body Schema = {repoUrl: str, prompt: str}

**Call TinyGen 2.0**

```POST /tiny_gen_two/call``` 

- Body Schema = {repoUrl: str, prompt: str}

## Fetch Supabase Data

**Fetch Past TinyGen 1.0 Calls From Supabase**

```GET /tiny_gen_one/get_past_calls``` 

**Fetch Past TinyGen 2.0 Calls From Supabase**

```GET /tiny_gen_two/get_past_calls``` 

## Docs
**Get API Docs**

```GET /tiny_gen_two/get_past_calls``` 
