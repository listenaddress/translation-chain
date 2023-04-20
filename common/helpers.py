import requests
from common.constants import *

def get_last_translation(chain):
    print("In here", chain.steps)
    for step in reversed(chain.steps[:chain.current_step]):
        print("step: ", step)
        if step["type"] == "translate":
            return step["output"]
        
def get_paper_on_semantic_scholar_by_id(id):
    url = SEMANTIC_SCHOLAR_GRAPH_API_URL + "paper/" + id
    params = {
        "fields": "title,authors,url,publicationDate,citationCount,externalIds,embedding"}
    response = requests.get(url, headers=ss_headers, params=params)
    if response.status_code == 200:
        return response.json()
