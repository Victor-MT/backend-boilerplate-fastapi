
from enum import Enum
import os
from anyio import Path
from datetime import datetime
    
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

    return Path() / 'env' / env_file
