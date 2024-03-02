import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def insert_to_supabase(prompt, repoUrl, response, tinygen_table_name):
    try:
        data, count = supabase.table(tinygen_table_name).insert({"prompt": prompt, "repoUrl": repoUrl, "response": response}).execute()
        return "success!"
    except:
        return "error"
    

def fetch_all_calls(tinygen_table_name):
    response = supabase.table(tinygen_table_name).select("*").execute()
    return response.json()