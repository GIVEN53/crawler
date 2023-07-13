from dotenv import load_dotenv
import os


# .env의 환경변수 값 읽기
def get_env(key):
    return os.environ.get(key)


load_dotenv()
