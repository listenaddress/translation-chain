from common.constants import base_prompt, openai, base_model

def get_last_translation(chain):
    for step in reversed(chain.steps[:chain.current_step]):
        if step["type"] == "translate":
            return step["output"]

def translate(chain):
    # Get the last finished step
    last_step = chain.steps[chain.current_step - 1]
    if last_step["type"] == 'get_neuroscience_concepts_and_possible_translations':
        prompt = base_prompt + \
          "Take this as context for the translation: " + last_step["output"] + \
          "Okay, now let's translate the following:" + \
          chain.input

        response = openai.ChatCompletion.create(
            model=base_model,
            messages=[
                {"role": "system", "content": prompt},
            ]
        )

        if response.choices and response.choices[0].message.content:
            print("Initial translation: " + response.choices[0].message.content)
            return response.choices[0].message.content
        else:
            raise Exception("No response from GPT for the translate step")
    elif last_step["type"] == 'critique':
        critiques = ""
        if chain.current_step > 1 and chain.steps[chain.current_step - 2]["type"] == "critique":
            critiques = chain.steps[chain.current_step - 2]["output"] + "\n\n" + last_step["output"]
        else:
            critiques = last_step["output"]
        
        last_translation = get_last_translation(chain)
        prompt = base_prompt + \
          "Ok, let's translate the following: " + \
          chain.input + \
          "Here's the last translation: " + \
          last_translation + \
          "Here's are critiques: " + \
          critiques + \
          "Ok, let's translate this again, this time taking into account the critiques."
        
        response = openai.ChatCompletion.create(
            model=base_model,
            messages=[
                {"role": "system", "content": prompt},
            ]
        )

        if response.choices and response.choices[0].message.content:
            print("Follow up translation after critiques: " + response.choices[0].message.content)
            return response.choices[0].message.content
    else:
        raise Exception("Last step not valid for translate step")
        