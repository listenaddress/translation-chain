import sys
from common.constants import *

def critique(chain):
    # Get the last finished step
    last_step = chain.steps[chain.current_step - 1]
    if last_step["type"] == "translate":
        print("Translating...")
        prompt = base_prompt + \
          "Actually, instead of translating something, let's critique the following translation. First, here's the original neuroscience: " + \
          chain.input + \
          "And here's the translation: " + \
          last_step["output"] + \
          "Let's critique this translation. What terms don't make sense in the context of developmental biology? What concepts aren't translating nicely? How might we improve this? Remember: this should fully make sense as a developmental biology abstract you'd see in a high-tier developmental biology journal. After answering those questions, provide an updated translation."
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
          raise Exception("No response from GPT-4 for the critique step")
    elif last_step["type"] == "critique":
        # Same as before but let's add "Let's critique this translation one more time. What terms don't make sense in the context of developmental biology? What concepts aren't translating nicely? How might we improve this? Remember: this should fully make sense as a developmental biology abstract you'd see in a high-tier developmental biology journal. After answering those questions, provide an updated translation. "
        print("Critiquing...")
        prompt = base_prompt + \
          "Actually, instead of translating something, let's critique the following translation. First, here's the original neuroscience: " + \
          chain.input + \
          "And here's the translation: " + \
          last_step["output"] + \
          "Here's the last critique: " + \
          last_step["output"] + \
          "Let's critique this translation one more time. What terms don't make sense in the context of developmental biology? What concepts aren't translating nicely? How might we improve this? What gramatical/conceptual mistakes are there? Remember: this should fully make sense as a developmental biology abstract you'd see in a high-tier developmental biology journal. After answering those questions, provide an updated translation that begins with 'TRANSLATION:'."
        
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
          raise Exception("No response from GPT-4 for a follow up critique step")