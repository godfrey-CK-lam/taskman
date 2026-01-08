# testing for supabase
import os

from typing import Final
from flask import Flask
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url: Final[str] = os.getenv('SUPABASE_URL')
pub_key: Final[str] = os.getenv('SUPABASE_PUBLISHABLE_KEY')
supabase: Client = create_client(url, pub_key)
response = supabase.table('tasks').select("*").execute()
instruments = response.data

print(instruments)

