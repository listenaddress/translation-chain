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
                  print("Starting ", step.type)
                  step.output = getattr(self, step.type)()
                  step.finished = True
                  self.steps[self.current_step] = asdict(step)
                  object.__setattr__(self, "current_step", self.current_step + 1)
                  self.save()
                  print("Finished ", step.type)
                except Exception as e:
                  print("Error in ", step.type)
                  print(e)
                  break
        
        print("Finished running translation chain")
    
    def get_neuroscience_concepts_and_possible_translations(self):
      return "They talk about the hippocampus and the amygdala. Theses could be translated to body and person." 


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
        # Step(type="find_relevant_papers"),
        # Step(type="summarize_relevance_of_papers"),
        # Step(type="summarize_best_translation_options"),
        # Step(type="translate"),
        # Step(type="find_relevant_papers_for_translation"),
        # Step(type="summarize_relevance_of_papers_for_translation"),
        # Step(type="adjust_abstract"),
        # Step(type="critique"),
        # Step(type="add_citations"),
        # Step(type="save_translation"),
        # Step(type="review_translation"),
    ]


