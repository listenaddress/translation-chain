from common.constants import base_prompt, openai

def translate(chain):
    # Get the last finished step
    last_step = chain.steps[chain.current_step - 1]
    if last_step["type"] == 'get_neuroscience_concepts_and_possible_translations':
        print("Finding neuroscience concepts and possible translations...")
        prompt = base_prompt + \
          "Take this as context for the translation: " + last_step["output"] + \
          "Okay, now let's translate the following:" + \
          chain.input
        print(prompt)

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
            ]
        )

        print(response)
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content
        else:
            raise Exception("No response from GPT-4 for the translate step")
    else:
        raise Exception("Last step not valid for translate step")
        