import requests

from common.constants import *
from common.helpers import get_last_translation


def find_and_summarize_relevant_papers(chain):
    last_step = chain.steps[chain.current_step - 1]

    if last_step["type"] == "get_neuroscience_concepts_and_possible_translations":
        natural_language_search_prompt_ending = "Don't translate anything yet. Let's find relevant papers to assist us. What topics should we get more information on to make a great translation? Where are our blind spots where we could use more information? What relationships between neuroscience and developmental biology should we look for? After considering these things, produce 5 natural language queries that could be used in an academic paper search engine."
        keyword_search_prompt_ending = "Don't translate anything yet. Let's find relevant papers to assist us. What topics should we get more information on to make a great translation? Where are our blind spots where we could use more information? What relationships between neuroscience and developmental biology should we look for? After considering these things, produce 5 separated keyword search queries. Take individual words in the keywords we're looking for and concat each one with a +. For example, if we're wondering how cell signaling relates to brain mapping, we could have the query 'cell+signaling+brain+mapping'. Notice how each word is separated by a +. This is how the separated by a plus with no spaces."
        find_relevant_papers_prompt = base_prompt + \
            "Here's the input abstract: " + \
            chain.input + \
            "[Abstract done] Some suggestions we can use if you want: " + last_step["output"] + \
            keyword_search_prompt_ending

        response = openai.ChatCompletion.create(
            model=base_model,
            messages=[
                {"role": "system", "content": find_relevant_papers_prompt},
            ]
        )

        if response.choices and response.choices[0].message.content:
            print("Find relevant papers response: " +
                  response.choices[0].message.content)
            get_five_queries_prompt = "Here is a previous response from GPT-4. It include 5 search queries. Please put them into a valid python list with no other words in your response. Just the python list. Each string in the list should have individual words separated by plus signs. I.e. 'What+is+cognition+and+where+is+it'. If there any spaces between words or plus signs remove them." + \
                response.choices[0].message.content
            final_five_queries = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": get_five_queries_prompt},
                ]
            )
            if final_five_queries.choices and final_five_queries.choices[0].message.content:
                final_five_queries_list = eval(
                    final_five_queries.choices[0].message.content)

                print("Final five queries: ", final_five_queries_list)

                papers = []
                paper_contexts = []
                relevant_summaries = []
                for query in final_five_queries_list:
                    response = requests.get(
                        "https://api.semanticscholar.org/graph/v1/paper/search?limit=4&query=" + query)
                    if response.status_code == 200:
                        print("Response: ", response.json())
                        papers += response.json()["data"]

                # Go get details on each paper
                for paper in papers:
                    try:
                        response = requests.get(
                            "https://api.semanticscholar.org/graph/v1/paper/" +
                            paper["paperId"],
                            headers={"Accept": "application/json"},
                            params={"fields": "title,abstract"}
                        )

                        if response.status_code == 200:
                            details = response.json()
                            if "abstract" in details and "title" in details:
                                print("Adding abstract")
                                paper_contexts.append(
                                    details["title"] + ": " + details["abstract"])
                        else:
                            print("Error getting paper details: ",
                                  response.status_code)

                    except Exception as e:
                        print("Error getting paper details: ", e)

                for context in paper_contexts[:5]:
                    prompt = minimal_prompt + \
                        "Don't worry about translating yet though." + \
                        "First, let's decide what the following paper may have to tell us about the translation. " + \
                        "If it's nothing, that's fine. But if it's relevant to making a good translation, let's summarize why it might be relevant. " + \
                        "Here's the abstract we're trying to translate: " + \
                        chain.input + \
                        "Here's some context for how we may want to transate it: " + \
                        last_step["output"] + \
                        "And here's the paper we're looking at to see if it say anything relevant we should keep in mind as we translate to developmental biology: " + \
                        context

                    response = openai.ChatCompletion.create(
                        model=base_model,
                        messages=[
                            {"role": "system", "content": prompt},
                        ]
                    )

                    if response.choices and response.choices[0].message.content:
                        print("Relevant summary response: " +
                              response.choices[0].message.content)
                        relevant_summaries.append(
                            response.choices[0].message.content)
                    else:
                        print("Error getting relevant summary")
                        print("Prompt: ", prompt)
                        raise Exception(
                            "No response from GPT for the find_and_summarize_relevant_papers step")

                # Concat all the summaries
                relevant_summaries = " ".join(relevant_summaries)
                summarize_summaries_prompt = "Here are a bunch of summaries and why they might be useful for a translation we're making. Can you concisely describe only the parts that are noteworthy." + \
                    relevant_summaries

                response = openai.ChatCompletion.create(
                    model=base_model,
                    messages=[
                        {"role": "system", "content": summarize_summaries_prompt},
                    ]
                )

                if response.choices and response.choices[0].message.content:
                    print("Summarized summaries response: " +
                          response.choices[0].message.content)
                    return response.choices[0].message.content
                else:
                    print("Error getting summarized summaries")
                    print("Prompt: ", summarize_summaries_prompt)
                    raise Exception(
                        "No response from GPT for the find_and_summarize_relevant_papers step")
            else:
                print("Error getting final five queries")
                print("Prompt: ", get_five_queries_prompt)
                raise Exception(
                    "No response from GPT for the find_and_summarize_relevant_papers step")

        else:
            raise Exception(
                "No response from GPT for the pull_neuroscience_concepts_and_describe_possible_translations step")
