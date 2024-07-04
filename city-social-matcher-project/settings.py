import dotenv # type: ignore
import os
import jotform_api
import json

def updateAPIKey(apikey):
    if apikey != '':
        if os.path.exists(".env") == False:
            f = open(".env", "w")
            f.write("API_KEY='" + apikey + "'")
            f.close()
        else:
            dotenv_file = dotenv.find_dotenv()
            dotenv.load_dotenv(dotenv_file)
            os.environ["API_KEY"] = apikey
            dotenv.set_key(dotenv_file, "API_KEY", os.environ["API_KEY"])
        return True
    else:
        return False

def getAPIKey():
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    return os.environ["API_KEY"]

def checkCurrentUser():
    # this is to be called when application is started

    # first see if there is a .env file
    if os.path.exists(".env") == False: # if not then make one
        f = open(".env", "w")
        f.write("API_KEY='changeme'")
        f.close()
    
    # if there is then check if the apikey is valid
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    apikey = dotenv.get_key(dotenv_file, "API_KEY")

    user = jotform_api.JotformAPI.getUser(apikey)
    if user == False:
        return False
    else:
        return user