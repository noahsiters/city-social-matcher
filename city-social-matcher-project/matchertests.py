import matcher
import jotform_api
import json
import submission
import operator

def test():
    # testGetSubmissions()
    testGetFormSubmissions()

def getMatches(people):
    males = []
    females = []

    responsesDict = {

    }

    for pers in people:
        if pers.getGender() == "male":
            males.append(pers)
        elif pers.getGender() == "female":
            females.append(pers)

    # adding combinations and scores to dictionary
    i = 0
    for female in females:
        for male in males:
            responsesDict[male.getFullName() + " + " + female.getFullName()] = str(matcher.getCompatibilityPercentage(male, female)) + "%"

    sorted_responsesDict = dict( sorted(responsesDict.items(), key=operator.itemgetter(1), reverse=True)) # reverse=True sorts in descending
    # print(sorted_responsesDict)
    return sorted_responsesDict

def testGetSubmissions():
    # formid = "241729074080152"
    # formid = "241778484441162"
    formid="241779041684161"
    responseString = matcher.getSubmissions(formid)
    print(responseString)

def testGetFormSubmissions():
    formid="241779041684161"
    submissions = jotform_api.JotformAPI.getFormSubmissions(formid) # returns a list of form submissions, each submission in dict format

    responsesDict = {

    }

    people = []
    males = []
    females = []

    # categories = ["Relationships", "Passions/Hobbies"]

    prettyJsonResponses = []

    # will need to dynamically create person objects based on the number of submissions between two dates
    for sub in submissions:
        json_object = json.dumps(sub, indent=2)
        # prettyJsonResponses.append(json_object)
        sub_json = json.loads(json_object)

        creationDate = sub_json["created_at"]

        # personal info
        firstName = ""
        lastName = ""
        email = ""
        age = ""
        gender = ""
        responses = []
        for answer in sub_json["answers"]:

            # check if answer is of type "control_matrix" (table that contains answers)
            if sub_json["answers"][answer]["type"] == "control_matrix":
                for key in sub_json["answers"][answer]["answer"]:
                    resp = sub_json["answers"][answer]["answer"][key]
                    # print(sub_json["answers"][answer]["answer"][key])
                    if resp == "Strongly Disagree":
                        responses.append(0)
                    elif resp == "Disagree":
                        responses.append(1)
                    elif resp == "Neither":
                        responses.append(2)
                    elif resp == "Agree":
                        responses.append(3)
                    elif resp == "Strongly Agree":
                        responses.append(4)
            # check if answer is personal info
            elif sub_json["answers"][answer]["name"] == "firstName":
                firstName = sub_json["answers"][answer]["answer"]
            elif sub_json["answers"][answer]["name"] == "lastName":
                lastName = sub_json["answers"][answer]["answer"]
            elif sub_json["answers"][answer]["name"] == "email":
                email = sub_json["answers"][answer]["answer"]
            elif sub_json["answers"][answer]["name"] == "age":
                age = sub_json["answers"][answer]["answer"]
            elif sub_json["answers"][answer]["name"] == "gender":
                gender = sub_json["answers"][answer]["answer"]


            # print(sub_json["answers"][answer]["answer"])
            # print(sub_json["answers"][answer]["text"])

            # get personal information
            # if "First Name" in sub_json["answers"][answer]["text"]:
            #     person["first-name"] = sub_json["answers"][answer]["answer"]
            # elif "Last Name" in sub_json["answers"][answer]["text"]:
            #     person["last-name"] = sub_json["answers"][answer]["answer"]

        # people.append(person)
        people.append(submission.Submission(firstName, lastName, email, age, gender, responses, creationDate))
        
        matches = getMatches(people)

        for key in matches:
            print(key + " : " + matches[key])
    # print(prettyJsonResponses[0])

    # for pers in people:
    #     print(pers.getFirstName() + pers.getLastName())
    #     print(pers.getResponses())

    # print(json_object)

test()