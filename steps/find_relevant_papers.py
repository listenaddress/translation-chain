from common.constants import *
from common.helpers import get_last_translation

def find_relevant_papers(chain):
    last_step = chain.steps[chain.current_step - 1]
    
    if last_step["type"] == "get_neuroscience_concepts_and_possible_translations":
        find_relevant_papers_prompt = base_prompt + \
            "Here's the input abstract: " + \
            chain.input + \
            "[Abstract done] Some suggestions we can use if you want: " + last_step["output"] + \
            "Don't translate anything yet. Let's find relevant papers to assist us. What topics should we get more information on to make a great translation? Where are our blind spots where we could use more information? What relationships between neuroscience and developmental biology should we look for? After considering these things, produce 5 natural language queries that could be used in an academic paper search engine."

        response = openai.ChatCompletion.create(
            model=base_model,
            messages=[
                {"role": "system", "content": find_relevant_papers_prompt},
            ]
        )

        if response.choices and response.choices[0].message.content:
            print("Find relevant papers response: " + response.choices[0].message.content)
            # Using GPT-3.5-turbo, the response is 5 queries, and put them into a list
            get_five_queries_prompt = "Here is a previous response from GPT-4. It include 5 search queries. Please put them into a valid python list with no other words in your response. Just the python list." + response.choices[0].message.content
            final_five_queries = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": get_five_queries_prompt},
                ]
            )
            if final_five_queries.choices and final_five_queries.choices[0].message.content:
                final_five_queries_list = eval(final_five_queries.choices[0].message.content)

            raise Exception("Not fully implemented yet")

        else:
            raise Exception("No response from GPT for the pull_neuroscience_concepts_and_describe_possible_translations step")