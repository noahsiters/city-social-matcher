import os
import dotenv # type: ignore

from jotform import JotformAPIClient # type: ignore

class JotformAPI:
    def getFormSubmissions(formId):
        dotenv.load_dotenv()

        jotformAPIClient = JotformAPIClient(os.getenv("API_KEY"))

        return jotformAPIClient.get_form_submissions(formId)
    
    def getUserForms():
        dotenv.load_dotenv()

        jotformAPIClient = JotformAPIClient(os.getenv("API_KEY"))

        return jotformAPIClient.get_forms()