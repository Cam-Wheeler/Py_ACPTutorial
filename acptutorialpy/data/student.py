# Standard Lib Imports:
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    student_id: str
    module: str = field(default="Applied Cloud Programming", init=False)