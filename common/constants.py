import os
from dotenv import load_dotenv, find_dotenv
from requests_oauthlib import OAuth1Session
import openai

load_dotenv(find_dotenv(), verbose=True)

SEMANTIC_SCHOLAR_GRAPH_API_URL = os.getenv("SEMANTIC_SCHOLAR_GRAPH_API_URL")
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
SEMANTIC_SCHOLAR_DATASETS_API_URL = os.getenv(
    "SEMANTIC_SCHOLAR_DATASETS_API_URL")

openai.api_key = os.getenv("OPEN_AI_API_KEY")

ss_headers = {'x-api-key': SEMANTIC_SCHOLAR_API_KEY}
