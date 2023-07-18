
from enum import Enum
import os
from anyio import Path
from datetime import datetime
import re
from typing import Union

def verify_margin(valor1, valor2, percent_margin):
    HasSomeNone = valor1 is None or valor2 is None

    if HasSomeNone:
        return False

    margem = valor1 * (percent_margin/100)
    
    return abs(valor1 - valor2) <= margem

def get_patterned_string(text, pattern, replace=None) -> Union[str, None]:
    if replace is not None:
        old_value, new_value = replace
    
    res = None
    match = re.search(pattern, text)

    if match:
        res = str(match.group())
        if replace:
            res = res.replace(old_value, new_value)

    return res

def int_to_str_format(value: int):
    if value < 10:
        return '0'+ value
    
    return value
    
class EnvironmentEnum(str, Enum):
    development = 'dev'
    staging = 'stg'
    production = 'prod'
    
def get_env():
    env = os.environ.get("environment")
    
    if env is None:
        env = 'development'

    return getattr(EnvironmentEnum, env.lower()).value

def get_env_file_path():
    env_file = get_env() + '.env'

    return Path() / 'core' /'env' / env_file

class Folder:
    def __init__(self, path):
        self.path = path
        self.folders: list[Folder] = []
        self.files: list[File] = []
        
    def add_folder(self, folder):
        self.folders.append(folder)
        
    def add_file(self, file):
        self.files.append(file)
        

class File:
    def __init__(self, path: Path):
        self.path = path
        self.path_string = path._str
    
    def get_created_date(self):
        return datetime.fromtimestamp(self.path.stat().st_ctime)
    
    def get_last_modified_date(self):
        return datetime.fromtimestamp(self.path.stat().st_mtime)
