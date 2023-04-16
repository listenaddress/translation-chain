import hashlib
import os
import time
import json

from common.constants import *
from dataclasses import dataclass, field, asdict

@dataclass(frozen=True)
class TranslationChain():
    created_at: float = field(default_factory=time.time)
    last_updated_at: float = field(default_factory=time.time)
    message: str = ""
    hash: str = ""
    current_step: int = 1
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
        if not self.hash:
            object.__setattr__(self, "hash", hashlib.sha256(self.message.encode('utf-8')).hexdigest())

    def save(self):
        file_path = f"cache/{self.hash}.json"
        with open(file_path, "w") as f:
            f.write(json.dumps(asdict(self)))

    @classmethod
    def load(cls, message):
        hash = hashlib.sha256(message.encode('utf-8')).hexdigest()
        file_path = f"cache/{hash}.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.loads(f.read())
            return cls(**data)
        else:
            new_translation = cls(message=message)
            new_translation.save()
            return new_translation
