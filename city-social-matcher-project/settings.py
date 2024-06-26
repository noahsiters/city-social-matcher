import dotenv # type: ignore
import os

def updateAPIKey(apikey):
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    print(os.environ["API_KEY"])
    os.environ["API_KEY"] = apikey
    print(os.environ["API_KEY"])

    dotenv.set_key(dotenv_file, "API_KEY", os.environ["API_KEY"])

def getAPIKey():
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    return os.environ["API_KEY"]