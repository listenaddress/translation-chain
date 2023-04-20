import sys
from common.constants import *

def get_neuroscience_concepts_and_possible_translations(chain):
  prompt = base_prompt + "GPT, Before making a full translation, take this abstract and describe in detail a few ways we could translate this. Specifically: - What are three major neuroscience concepts in this abstract? - For those three concepts, what are three real concepts you can find in developmental biology literature that could make sense as translations? And why do these translations make sense? Abstract here:"
  prompt += chain.input

  response = openai.ChatCompletion.create(
      model=base_model,
      messages=[
          {"role": "system", "content": prompt},
      ]
  )

  if response.choices and response.choices[0].message.content:
      print("Neuroscience concepts and possible translations: " + response.choices[0].message.content)
      return response.choices[0].message.content
  else:
      raise Exception("No response from GPT for the pull_neuroscience_concepts_and_describe_possible_translations step")
