
# Welcome To The TinyGen Repo!

## Useful Links

- [TinyGen UI](https://tiny-gen.streamlit.app/)
- [TinyGen Project Overview](https://tawsifkamal.notion.site/TinyGen-3bc759c6254a4e33ad7f7fac86d97c0b?pvs=74)
- [Production API Base Url](https://tiny-gen-zbkbev3qaq-uc.a.run.app)


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
streamlit run frontend/TinyGen.py
```

# Making API Calls Directly
The following endpoints are available when making api calls. A public workspace on postman is linked [here](https://elements.getpostman.com/redirect?entityId=17857495-f27f8dae-edd0-4a36-8382-809507a65587&entityType=collection)

**Full link**

https://elements.getpostman.com/redirect?entityId=17857495-f27f8dae-edd0-4a36-8382-809507a65587&entityType=collection

Otherwise, feel free to call the APIs yourself using your preferred API client. The endpoints are listed below:

If using local API, base_url = ```http://localhost:8000```

If using prod API, base_url = ```https://tiny-gen-zbkbev3qaq-uc.a.run.app```
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
