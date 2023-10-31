from dataclasses import dataclass

@dataclass
class Bot:
    token:str
    admin:str

@dataclass
class Database:
    user:str
    password:str
    host:str
    port:int
    db:str