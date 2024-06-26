import json
import os
import dotenv

from jotform import JotformAPIClient

class JotformAPI:
    def getResponses(formId):
        dotenv.load_dotenv()
        jotformAPIClient = JotformAPIClient(os.getenv("API_KEY"))
        print(os.getenv("API_KEY"))

        submissions = jotformAPIClient.get_form_submissions(formId)

        quizResponsesDict = {

        }

        for submission in submissions:
            json_object = json.dumps(submission, indent=2)
            submission_json = json.loads(json_object)

            for answer in submission_json["answers"]:
                if "quiz" in submission_json["answers"][answer]["name"]:
                    quizResponsesDict[submission_json["answers"][answer]["text"]] = submission_json["answers"][answer]["answer"] # stuffs value from "answer" item into dict

        responseString = ""
        for key in quizResponsesDict:
            responseString += key + " : " + quizResponsesDict[key] + "\n"

        print(responseString)
        return responseString