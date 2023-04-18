import hashlib
import os
import time
import json

from common.constants import *  
from dataclasses import dataclass, field, asdict
from typing import List, Union, Any

@dataclass
class Step:
    type: str
    output: Any = None
    finished: bool = False

@dataclass(frozen=True)
class TranslationChain():
    created_at: float = field(default_factory=time.time)
    last_updated_at: float = field(default_factory=time.time)
    finished_at: float = None
    message: str = ""
    target_domain: str = ""
    hash: str = ""
    current_step: int = 0
    steps: list[Step] = field(default_factory=list)
    calls_to_gpt: list = field(default_factory=list)
    neuroscience_concepts: list = field(default_factory=list)
    possible_translations: list = field(default_factory=list)
    relevant_papers: list = field(default_factory=list)
    relevant_papers_summary: str = ""
    best_translation_options: list = field(default_factory=list)
    initial_translation: str = ""
    initial_translation_relevant_papers: list = field(default_factory=list)
    initial_translation_relevant_papers_summary: str = ""
    final_translation: str = ""

    def __post_init__(self):
        if not self.message:
            raise ValueError("Message is required")
        if not self.steps:
            object.__setattr__(self, "steps", get_default_steps())
        if not self.hash:
            object.__setattr__(self, "hash", hashlib.sha256(self.message.encode('utf-8')).hexdigest())
        if not self.target_domain:
            object.__setattr__(self, "target_domain", "developmental biology")

    def save(self):
        file_path = f"cache/{self.hash}.json"
        with open(file_path, "w") as f:
            f.write(json.dumps(asdict(self)))
    
    def run(self):
        for step in self.steps:
            if isinstance(step, dict):
                step = Step(**step)

            if not step.finished:
                try:
                  step.output = getattr(self, step.type)()
                  step.finished = True
                  self.steps[self.current_step] = asdict(step)
                  object.__setattr__(self, "current_step", self.current_step + 1)
                  if self.current_step == len(self.steps):
                    object.__setattr__(self, "finished_at", time.time())
                  self.save()
                  print("Finished ", step.type)
                except Exception as e:
                  print("Error in ", step.type)
                  print(e)
                  break
        
        
    
    def get_neuroscience_concepts_and_possible_translations(self):
      return "They talk about the hippocampus and the amygdala. Theses could be translated to body and person." 

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
    
    def translate(self):
      return "The body and the person are important for memory"
    
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
    
    def critique(self):
        return "After reviewing the translation, I think it is good to go"
    
    def get_final_translation(self):
        object.__setattr__(self, "final_translation", "The body and the person are important for memory")
        return "Final translation: The body and the person are important for memory"

    @classmethod
    def load(cls, message=message, hash=hash):
        if hash:
            file_path = f"cache/{hash}.json"
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.loads(f.read())
                chain = cls(**data)
                for step in chain.steps:
                    step = Step(**step)
                return chain
            else:
                raise ValueError("No translation chain found for hash")
            
        hash = hashlib.sha256(message.encode('utf-8')).hexdigest()
        file_path = f"cache/{hash}.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.loads(f.read())
            chain = cls(**data)

            return chain
        else:
            new_translation = cls(message=message)
            new_translation.save()
            return new_translation


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
        Step(type="get_final_translation")
    ]
