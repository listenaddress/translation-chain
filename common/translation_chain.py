import hashlib
import os
import time
import json
from dataclasses import dataclass, field, asdict

from common.constants import *
from common.helpers import get_default_steps, get_minimal_steps
from common.step import Step
from steps.get_neuroscience_concepts_and_possible_translations import get_neuroscience_concepts_and_possible_translations
from steps.translate import translate
from steps.critique import critique
from steps.find_and_summarize_relevant_papers import find_and_summarize_relevant_papers


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
            object.__setattr__(self, "steps", get_default_steps())
        if not self.id:
            object.__setattr__(self, "id", hashlib.sha256(
                self.input.encode('utf-8')).hexdigest())

    def run(self):
        for step in self.steps[self.current_step:]:
            try:
                if isinstance(step, dict):
                    step = Step(**step)

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

    def save(self):
        file_path = f"cache/{self.id}.json"
        with open(file_path, "w") as f:
            f.write(json.dumps(asdict(self)))

    def get_neuroscience_concepts_and_possible_translations(self):
        return get_neuroscience_concepts_and_possible_translations(self)

    def translate(self):
        return translate(self)

    def critique(self):
        return critique(self)

    def find_and_summarize_relevant_papers(self):
        return find_and_summarize_relevant_papers(self)

    def summarize_relevance_of_papers(self):
        return "The hippocampus and the amygdala are important for memory"

    @classmethod
    def load(cls, input=input):
        id = hashlib.sha256(input.encode('utf-8')).hexdigest()
        file_path = f"cache/{id}.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.loads(f.read())
            return cls(**data)

        new_translation = cls(input=input)
        new_translation.save()
        return new_translation

    @classmethod
    def loadById(cls, id=id):
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
