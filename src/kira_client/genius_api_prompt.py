from langchain import PromptTemplate
from langchain.chains.api.prompt import API_URL_PROMPT_TEMPLATE

GENIUS_API_DOCS = """API documentation:
Endpoint: https://api.genius.com
GET /search

This API is for searching music artists, albums, or tracks.

Query parameters table:
q | string | Search term, e.g., artist name, album title, track title | required

Response schema (JSON object):
hits | array[object] (Artist / Album / Track Result Object)

Each object in the "hits" key has the result property with following schema:
api_path | string | The API path to the result, e.g., /songs/5466416.
artist_names | string | The name of the artist. eg., "LeanJe".
title | string | The full title of the result, e.g., "Идеальный пациент".
"""

_API_RESPONSE_PROMPT_TEMPLATE = (
    API_URL_PROMPT_TEMPLATE
    + """ {api_url}

Here is the response from the API:

{api_response}

Summarize this response to answer the original question. 
From response you should extract only first item from hits results array.
You should provide me a response in valid JSON format with the following fields - track_id, artist_name and song_name
From song name you should remove all track translations in brackets, e.g. "Идеальный пациент (Perfect Patient)" -> "Идеальный пациент"

JSON output:"""
)

GENIUS_API_RESPONSE_PROMPT = PromptTemplate(
    input_variables=["api_docs", "question", "api_url", "api_response"],
    template=_API_RESPONSE_PROMPT_TEMPLATE,
)
