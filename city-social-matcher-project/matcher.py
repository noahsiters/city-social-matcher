import operator
import jotform_api
import json
import submission
    
# define methods
# this method will combine each persons answers to see how similar they are, and give it a percentage of similarity
def getCompatibilityPercentage(male, female):
    maleResp = male.getResponses()
    femaleResp = female.getResponses()

    percentages = []

    k = 0
    while k < len(maleResp):
        if maleResp[k] == femaleResp[k]: # if responses are exact
            percentages.append(1)
        elif abs(maleResp[k] - femaleResp[k]) == 1: # if responses are 1 away
            percentages.append(.75)
        elif abs(maleResp[k] - femaleResp[k]) == 2: # if responses are 2 away
            percentages.append(.5)
        elif abs(maleResp[k] - femaleResp[k]) == 3: # if responses are 3 away
            percentages.append(.25)
        elif abs(maleResp[k] - femaleResp[k]) == 4: # if responses are opposite
            percentages.append(0)
        k += 1

    return round((sum(percentages) / len(percentages)) * 100) # get the average percentage and move it one decimal

# this method will get all of the combinations and organize them in a single dictionary, then sort in descending order
def getMatches(formid):
    parsedSubmissions = getDataFromSubmissions(formid)

    males = []
    females = []

    responsesDict = { }

    # sort each submission into male and female lists
    for parsedSub in parsedSubmissions:
        if parsedSub.getGender() == "male":
            males.append(parsedSub)
        elif parsedSub.getGender() == "female":
            females.append(parsedSub)
        
    # adding combinations and scores to dictionary
    for female in females:
        for male in males:
            responsesDict[male.getFullName() + " + " + female.getFullName()] = str(getCompatibilityPercentage(male, female)) + "%"

    sorted_responsesDict = dict( sorted(responsesDict.items(), key=operator.itemgetter(1), reverse=True)) # reverse=True sorts in descending

    responseStr = "MATCHES:\n"
    for key in sorted_responsesDict:
        responseStr += key + " : " + sorted_responsesDict[key] + "\n"

    return responseStr

# gets submissions from json API class
def getDataFromSubmissions(formId):
    submissions = jotform_api.JotformAPI.getFormSubmissions(formId)

    parsedSubmissions = []

    for sub in submissions:
        json_object = json.dumps(sub, indent=2) # converts to json and makes it pretty
        sub_json = json.loads(json_object) # makes json parsable

        # submission data
        firstName = ""
        lastName = ""
        email = ""
        age = ""
        gender = ""
        responses = []
        creationDate = sub_json["created_at"]
        for answer in sub_json["answers"]:

            # checks if answer is of type "control_matrix" (table that contains answers)
            if sub_json["answers"][answer]["type"] == "control_matrix":
                for key in sub_json["answers"][answer]["answer"]:
                    resp = sub_json["answers"][answer]["answer"][key]
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
        
        parsedSubmissions.append(submission.Submission(firstName, lastName, email, age, gender, responses, creationDate))

    return parsedSubmissions

def getListOfUserForms():
    forms = jotform_api.JotformAPI.getUserForms()

    parsedForms = {

    }

    for form in forms:
        json_object = json.dumps(form, indent=2)
        form_json = json.loads(json_object)

        # form data
        formTitle = form_json["title"]
        formId = form_json["id"]
        status = form_json["status"]

        if status == "ENABLED":
            parsedForms[formId] = formTitle

    # print(parsedForms)
    return list(parsedForms.values())

def getFormIdBasedOnFormTitle(arg):
    forms = jotform_api.JotformAPI.getUserForms()

    parsedForms = {

    }

    for form in forms:
        json_object = json.dumps(form, indent=2)
        form_json = json.loads(json_object)

        # form data
        formTitle = form_json["title"]
        formId = form_json["id"]
        status = form_json["status"]

        if status == "ENABLED":
            parsedForms[formId] = formTitle

    return list(parsedForms.keys())[list(parsedForms.values()).index(arg)]


# --- sample input ---
# responses = [0, 1, 2, 3, 4]

# responsesDict = {

# }

# pAdam = Person("Adam", [responses[0], responses[4], responses[2], responses[2], responses[3]], 4405552222, "adamanderson@test.com")
# pBill = Person("Bill", [responses[2], responses[2], responses[1], responses[3], responses[4]], 4405551234, "billwilly@test.com")
# pCarl = Person("Carl", [responses[0], responses[4], responses[2], responses[2], responses[3]], 4405554321, "carlcarter@test.com")
# pDan = Person("Dan", [responses[1], responses[2], responses[3], responses[3], responses[1]], 4405555543, "dandonaldson@test.com")

# pAlly = Person("Ally", [responses[4], responses[3], responses[3], responses[0], responses[2]], 4405552814, "allyarlington@test.com")
# pBeth = Person("Beth", [responses[2], responses[2], responses[3], responses[3], responses[1]], 4405558053, "bethbarry@test.com")
# pCait = Person("Cait", [responses[0], responses[2], responses[1], responses[1], responses[2]], 4405550932, "caitcarrington@test.com")
# pDina = Person("Dina", [responses[2], responses[3], responses[2], responses[2], responses[0]], 4405559021, "dinadomino@test.com")

# males = [pAdam, pBill, pCarl, pDan]
# females = [pAlly, pBeth, pCait, pDina]