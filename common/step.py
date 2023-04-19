import hashlib
import os
import time
import json

from common.constants import *
from dataclasses import dataclass, field, asdict

@dataclass
class Step:
    type: str
    output: any = None
    finished: bool = False
