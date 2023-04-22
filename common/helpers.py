import requests
from common.constants import *
from common.step import Step


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


def get_minimal_steps():
    return [
        Step(type="get_neuroscience_concepts_and_possible_translations"),
        Step(type="translate"),
        Step(type="critique"),
        Step(type="critique"),
        Step(type="translate")
    ]


def get_steps_with_look_up():
    return [
        Step(type="get_neuroscience_concepts_and_possible_translations"),
        Step(type="find_and_summarize_relevant_papers"),
        Step(type="translate"),
        Step(type="critique"),
        Step(type="critique"),
        Step(type="translate")
    ]


def get_steps_with_two_look_ups():
    return [
        Step(type="get_neuroscience_concepts_and_possible_translations"),
        Step(type="find_and_summarize_relevant_papers"),
        Step(type="translate"),
        Step(type="critique"),
        Step(type="critique"),
        Step(type="translate"),
        Step(type="find_and_summarize_relevant_papers"),
        Step(type="translate")
    ]


def get_chat_completion(prompt, model=base_model):
    return openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
        ]
    )
