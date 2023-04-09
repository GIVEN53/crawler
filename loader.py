from dotenv import load_dotenv
import os

load_dotenv()


def get_value(env):
    return os.environ.get(env)
