import sys
from common.constants import *

def get_last_translation(chain):
    print("In here", chain.steps)
    for step in reversed(chain.steps[:chain.current_step]):
        print("step: ", step)
        if step["type"] == "translate":
            return step["output"]

def critique(chain):
    last_step = chain.steps[chain.current_step - 1]
    last_translation = get_last_translation(chain)
    critique_prompt = base_prompt + \
        "Actually, instead of translating something, let's critique the following translation. Here's the original neuroscience: " + \
        chain.input + \
        "And here's the translation: " + \
        last_translation + \
        "Ok, let's critique that translation in detail. What terms don't make sense as developmental biology? What concepts aren't translating nicely? Are there gramatical/conceptual mistakes? How might we improve this? Remember: we're trying to apply the insights of the input into a new domain. The output should make sense as a developmental biology abstract you'd see in a high-tier developmental biology journal. Don't worry about providing a follow up translation, just give a detailed critique, as if you were a top-tier biology professor."

    if last_step["type"] == "translate":
        print("Critique prompt: ", critique_prompt)
        response = openai.ChatCompletion.create(
            model=base_model,
            messages=[
                {"role": "system", "content": critique_prompt},
            ]
        )

        if response.choices and response.choices[0].message.content:
            print("Critique: " + response.choices[0].message.content)
            return response.choices[0].message.content
        else:
          raise Exception("No response from GPT for the critique step")
    elif last_step["type"] == "critique":
        critique_prompt += "Here's a prior critique: " + \
          last_step["output"] + \
          "Ok, create an new critique for the translation in detail and do not repeat what is above in the prior critique. Make new suggestions."
        print("Critique prompt: ", critique_prompt)
        
        response = openai.ChatCompletion.create(
            model=base_model,
            messages=[
                {"role": "system", "content": critique_prompt},
            ]
        )

        if response.choices and response.choices[0].message.content:
            print("\nCritique: " + response.choices[0].message.content)
            return response.choices[0].message.content
        else:
          raise Exception("No response from GPT for a follow up critique step")