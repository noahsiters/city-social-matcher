import os
import dotenv # type: ignore

from jotform import JotformAPIClient # type: ignore

class JotformAPI:
    def getJotformData(formid):
        dotenv.load_dotenv()

        jotformAPIClient = JotformAPIClient(os.getenv("API_KEY"))

        submissions = jotformAPIClient.get_form_submissions(formid)
        questions = jotformAPIClient.get_form_questions(formid)

        return [submissions, questions]

    def getFormSubmissions(formId):
        dotenv.load_dotenv()

        jotformAPIClient = JotformAPIClient(os.getenv("API_KEY"))

        return jotformAPIClient.get_form_submissions(formId)
    
    def getUserForms():
        dotenv.load_dotenv()

        jotformAPIClient = JotformAPIClient(os.getenv("API_KEY"))

        return jotformAPIClient.get_forms()
    
    def getUser(apikey):
        jotformAPIClient = JotformAPIClient(apikey)

        try:
            user = jotformAPIClient.get_user()
            return user
        except:
            return False
        
    def getFormQuestions(formid):
        dotenv.load_dotenv()

        jotformAPIClient = JotformAPIClient(os.getenv("API_KEY"))

        return jotformAPIClient.get_form_questions(formid)