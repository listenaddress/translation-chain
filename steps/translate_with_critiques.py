import sys
from common.constants import *

def translate_with_critiques(chain):
    # Get all all steps that inclde "critique"
    critique_steps = [step for step in chain.steps if "critique" in step["type"]]
    print(critique_steps)
    
    #     prompt = base_prompt + \
    #       "Take this as context for the translation: " + last_step["output"] + \
    #       "Okay, now let's translate the following:" + \
    #       chain.input
    #     print(prompt)

    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": prompt},
    #         ]
    #     )

    #     print(response)
    #     if response.choices and response.choices[0].message.content:
    #         return response.choices[0].message.content
    #     else:
    #         raise Exception("No response from GPT-4 for the translate step")
    # else:
    raise Exception("Tttttt")
        