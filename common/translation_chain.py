import hashlib
import os
import time
import json
from dataclasses import dataclass, field, asdict
from typing import List, Union, Any

from common.constants import *  
from common.step import Step
from steps.get_neuroscience_concepts_and_possible_translations import get_neuroscience_concepts_and_possible_translations
from steps.translate import translate
from steps.critique import critique
from steps.translate_with_critiques import translate_with_critiques


@dataclass(frozen=True)
class TranslationChain():
    id: str = ""
    created: float = field(default_factory=time.time)
    finished: float = None
    input: str = ""
    output: str = ""
    target_domain: str = "developmental biology"
    current_step: int = 0
    steps: list[Step] = field(default_factory=list)
    

    def __post_init__(self):
        if not self.input:
            raise ValueError("input is required")
        if not self.steps:
            object.__setattr__(self, "steps", get_minimal_steps())
        if not self.id:
            object.__setattr__(self, "id", hashlib.sha256(self.input.encode('utf-8')).hexdigest())

    def save(self):
        file_path = f"cache/{self.id}.json"
        with open(file_path, "w") as f:
            f.write(json.dumps(asdict(self)))
    
    def run(self):
        # Loop over all steps that aren't finished
        for step in self.steps[self.current_step:]:
            if isinstance(step, dict):
                step = Step(**step)

            if not step.finished:
                try:
                  step.output = getattr(self, step.type)()
                  if step.output is None:
                      raise Exception("Output is None for step " + step.type)

                  step.finished = True
                  self.steps[self.current_step] = asdict(step)
                  object.__setattr__(self, "current_step", self.current_step + 1)
                  if self.current_step == len(self.steps):
                    object.__setattr__(self, "finished", time.time())
                  self.save()
                  print("Finished ", step.type)
                except Exception as e:
                  print("Error in ", step.type)
                  print(e)
                  break
        
        print("Run function complete.")
        
        
    
    def get_neuroscience_concepts_and_possible_translations(self):
      return get_neuroscience_concepts_and_possible_translations(self)
    
    def translate(self):
      return translate(self)
    
    def critique(self):
      return critique(self)
    
    def translate_with_critiques(self):
      return translate_with_critiques(self)

    def find_relevant_papers(self):
      return [
        {
          "title": "The hippocampus and the amygdala are important for memory",
          "abstract": "The hippocampus and the amygdala are important for memory",
          "url": "https://www.semanticscholar.org/paper/The-hippocampus-and-the-amygdala-are-important-for-Blair/7b9f1c8f7f8b0d7e7a2c2e8d1b0c2b4e0b4a9c8d"
        },
        {
          "title": "The hippocampus and the amygdala are important for memory",
          "abstract": "The hippocampus and the amygdala are important for memory",
          "url": "https://www.semanticscholar.org/paper/The-hippocampus-and-the-amygdala-are-important-for-Blair/7b9f1c8f7f8b0d7e7a2c2e8d1b0c2b4e0b4a9c8d"
        }
      ]
    
    def summarize_relevance_of_papers(self):
      return "The hippocampus and the amygdala are important for memory"
    
    def summarize_best_translation_options(self):
      return "The best options for translating the hippocampus and the amygdala are body and person"
    
    def find_relevant_papers_for_translation(self):
        return [
            {
                "title": "Memory and the hippocampus: a synthesis from findings with rats, monkeys, and humans",
                "abstract": "The hippocampus and the amygdala are important for memory",
                "url": "https://www.semanticscholar.org/paper/The-hippocampus-and-the-amygdala-are-important-for-Blair/7b9f1c8f7f8b0d7e7a2c2e8d1b0c2b4e0b4a9c8d"
            },
            {
                "title": "When memory fails: the role of the hippocampus in amnesia",
                "abstract": "The hippocampus and the amygdala are important for memory",
                "url": "https://www.semanticscholar.org/paper/The-hippocampus-and-the-amygdala-are-important-for-Blair/7b9f1c8f7f8b0d7e7a2c2e8d1b0c2b4e0b4a9c8d"
            }
        ]
    
    def summarize_relevance_of_papers_for_translation(self):
        return "The hippocampus and the amygdala are important for memory"
    
    def adjust_abstract(self):
        return "The body and the person are important for memory"
    
    def critique_again(self):
        return "After reviewing the translation again, I think it is good to go"
    
    def get_output(self):
        object.__setattr__(self, "output", "The body and the person are important for memory")
        return "Final translation: The body and the person are important for memory"

    @classmethod
    def load(cls, input=input, id=id):
        if id:
            file_path = f"cache/{id}.json"
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.loads(f.read())
                chain = cls(**data)
                for step in chain.steps:
                    step = Step(**step)
                return chain
            else:
                raise ValueError("No translation chain found for id")
            
        id = hashlib.sha256(input.encode('utf-8')).hexdigest()
        file_path = f"cache/{id}.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.loads(f.read())
            chain = cls(**data)

            return chain
        else:
            new_translation = cls(input=input)
            new_translation.save()
            return new_translation
        
    @classmethod
    def get_finished_chains(cls):
        chains = []
        for file in os.listdir("cache"):
            if file.endswith(".json"):
                with open(f"cache/{file}", "r") as f:
                    data = json.loads(f.read())
                chain = cls(**data)
                if chain.finished:
                    chains.append(chain)
        return chains

def get_minimal_steps():
    return [
        Step(type="get_neuroscience_concepts_and_possible_translations"),
        Step(type="translate"),
        Step(type="critique"),
        Step(type="critique")
    ]

def get_default_steps():
    return [
        Step(type="get_neuroscience_concepts_and_possible_translations"),
        Step(type="find_relevant_papers"),
        Step(type="summarize_relevance_of_papers"),
        Step(type="summarize_best_translation_options"),
        Step(type="translate"),
        Step(type="find_relevant_papers_for_translation"),
        Step(type="summarize_relevance_of_papers_for_translation"),
        Step(type="adjust_abstract"),
        Step(type="critique"),
        Step(type="get_output")
    ]
