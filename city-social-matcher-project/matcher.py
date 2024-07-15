import operator
import jotform_api
import json
import submission
import paired_submission
    
# define methods
# this method will combine each persons answers to see how similar they are, and give it a percentage of similarity
# TODO put in a swapper to make sure we get the best possible list of matches (maybe compare matches with other matches to see which is better)
# TODO or try stable marriage problem with gale shapely algorithm
def getCompatibilityPercentage(male, female):
    maleResp = male.getResponses()
    femaleResp = female.getResponses()

    percentages = []

    # k = 0
    # while k < len(maleResp):
    #     if maleResp[k] == femaleResp[k]: # if responses are exact
    #         percentages.append(1)
    #     elif abs(maleResp[k] - femaleResp[k]) == 1: # if responses are 1 away
    #         percentages.append(.75)
    #     elif abs(maleResp[k] - femaleResp[k]) == 2: # if responses are 2 away
    #         percentages.append(.5)
    #     elif abs(maleResp[k] - femaleResp[k]) == 3: # if responses are 3 away
    #         percentages.append(.25)
    #     elif abs(maleResp[k] - femaleResp[k]) == 4: # if responses are opposite
    #         percentages.append(0)
    #     k += 1

    for keyM in maleResp:
        for keyF in femaleResp:
            if keyM == keyF: # only comparing IF the question is the same
                # print(keyM + " : " + keyF)
                if maleResp[keyM] == femaleResp[keyF]: # if exact
                    percentages.append(1)
                elif abs(maleResp[keyM] - femaleResp[keyF]) == 1: # if 1 away
                    percentages.append(.75)
                elif abs(maleResp[keyM] - femaleResp[keyF]) == 2: # if 2 away
                    percentages.append(.50)
                elif abs(maleResp[keyM] - femaleResp[keyF]) == 3: # if 3 away
                    percentages.append(.25)
                elif abs(maleResp[keyM] - femaleResp[keyF]) == 4: # if opposite
                    percentages.append(0)

    return round((sum(percentages) / len(percentages)) * 100) # get the average percentage and move it one decimal

# this method will get all of the combinations and organize them in a single dictionary, then sort in descending order
def getMatches(formid):
    parsedSubmissions = parseDataFromSubmissions(formid)

    # for parsedSub in parsedSubmissions:
    #     print(parsedSub.getFullName())
    #     print(parsedSub.getGender())

    males = []
    females = []

    responsesDict = { }

    # sort each submission into male and female lists
    for parsedSub in parsedSubmissions:
        if parsedSub.getGender() == "Male":
            males.append(parsedSub)
        elif parsedSub.getGender() == "Female":
            females.append(parsedSub)
        
    possibleMatches = []
    matchesDict = {}

    for female in females:
        for male in males:
            # create a new paried_submission object (a match of two submission objects) and store it in the possibleMatches list
            possibleMatches.append(paired_submission.PairedSubmission(male, female))

    # for every possible match, store it in a dictionary with itself as the key and the compatibility percentage as the value
    # (this is so we can sort it from highest to lowest percentage
    for match in possibleMatches:
        matchesDict[match] = str(match.getPercentageOfSimilarAnswers()) + "%"

    # sorts the dictionary from highest to lowest value
    sorted_matchesDict = dict( sorted(matchesDict.items(), key=operator.itemgetter(1), reverse=True))

    # for match in sorted_matchesDict:
    #     print(match.getNamesAsString() + sorted_matchesDict[match])

    uniqueMatchesDict = { }
    matchedFemales = []
    matchedMales = []

    for key in sorted_matchesDict:
        # going from highest percentage to lowest, if a male or female has already been matched, then skip, otherwise they are matched
        if key.getFemale() not in matchedFemales and key.getMale() not in matchedMales:
            uniqueMatchesDict[key] = sorted_matchesDict[key]
            matchedFemales.append(key.getFemale()) # add female to list of matched females
            matchedMales.append(key.getMale()) # add male to list of matched males

    for key in uniqueMatchesDict:
        print(key.getNamesAsString() + " : " + uniqueMatchesDict[key])

    responseStr = "MATCHES:\n"
    for key in uniqueMatchesDict:
        responseStr += key.getNamesAsString() + " : " + uniqueMatchesDict[key] + "\n"

    return responseStr

# gets submissions from json API class
def parseDataFromSubmissions(formId):
    submissions = jotform_api.JotformAPI.getFormSubmissions(formId)

    parsedSubmissions = []

    for sub in submissions:
        json_object = json.dumps(sub, indent=2) # converts to json and makes it pretty
        sub_json = json.loads(json_object) # makes json parsable

        # print(json_object)

        # submission data
        firstName = ""
        lastName = ""
        email = ""
        age = ""
        gender = ""
        responses = []
        responsesDict = {}
        creationDate = sub_json["created_at"]

        for answer in sub_json["answers"]:

            # TODO combine the key and value of answer to allow for extra check that we are comparing the same questions
            # checks if answer is of type "control_matrix" (table that contains answers)
            if sub_json["answers"][answer]["type"] == "control_matrix":
                for key in sub_json["answers"][answer]["answer"]:
                    resp = sub_json["answers"][answer]["answer"][key]
                    if resp == "Strongly Disagree":
                        responses.append(0)
                        responsesDict[key] =  0
                    elif resp == "Disagree":
                        responses.append(1)
                        responsesDict[key] =  1
                    elif resp == "Neither":
                        responses.append(2)
                        responsesDict[key] =  2
                    elif resp == "Agree":
                        responses.append(3)
                        responsesDict[key] =  3
                    elif resp == "Strongly Agree":
                        responses.append(4)
                        responsesDict[key] =  4
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
                try:
                    gender = sub_json["answers"][answer]["answer"]
                except:
                    gender = "NULL"
        parsedSubmissions.append(submission.Submission(firstName, lastName, email, age, gender, responsesDict, creationDate))

    return parsedSubmissions

def getListOfUserForms():
    # TODO form could be condensed into its own object
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