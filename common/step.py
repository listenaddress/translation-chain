import hashlib
import os
import time
import json

from common.constants import *
from dataclasses import dataclass, field, asdict

@dataclass(frozen=True)
class Step():
    created_at: float = field(default_factory=time.time)
    output: any = ""
    
    def run(self):
        pass
