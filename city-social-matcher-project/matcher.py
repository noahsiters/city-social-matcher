import operator
import jotform_api
import json
import submission
import random
    
# this method will combine each persons answers to see how similar they are, and give it a percentage of similarity
def generatePercentageOfSimilarAnswers(personA, personB):
        responsesA = personA.getResponses()
        responsesB = personB.getResponses()

        percentages = []

        for keyM in responsesA:
            for keyF in responsesB:
                if keyM == keyF: # only comparing IF the question is the same
                    # print(keyM + " : " + keyF)
                    if responsesA[keyM] == responsesB[keyF]: # if exact
                        percentages.append(1)
                    elif abs(responsesA[keyM] - responsesB[keyF]) == 1: # if 1 away
                        percentages.append(.75)
                    elif abs(responsesA[keyM] - responsesB[keyF]) == 2: # if 2 away
                        percentages.append(.50)
                    elif abs(responsesA[keyM] - responsesB[keyF]) == 3: # if 3 away
                        percentages.append(.25)
                    elif abs(responsesA[keyM] - responsesB[keyF]) == 4: # if opposite
                        percentages.append(0)

        return round((sum(percentages) / len(percentages)) * 100) # get the average percentage and move it one decimal

# generates a list of most preferred to least preferred based on how similar their answers are
def generatePreferenceList(submission, suitors):
    preferences = []
    preferencesDict = {}
    for suitor in suitors:
        preferencesDict[suitor] = generatePercentageOfSimilarAnswers(submission, suitor)

    preferences_sorted_desc = dict( sorted(preferencesDict.items(), key=operator.itemgetter(1), reverse=True))

    for key in preferences_sorted_desc:
        preferences.append(key)

    return preferences

# this method solves the stable marriage problem using the Gale-Shapely algorithm
def getStableMarriages(submissions):
    listOfMales = []
    listOfFemales = []

    responseStr = ""

    for sub in submissions:
        if sub.getGender() == "Male":
            listOfMales.append(sub)
        elif sub.getGender() == "Female":
            listOfFemales.append(sub)

    if len(listOfMales) == len(listOfFemales):
        males_free = list(listOfMales)
        females_free = list(listOfFemales)
        
        # get preference lists for each male and female
        for male in listOfMales:
            male.setPreferenceList(generatePreferenceList(male, listOfFemales))

        for female in listOfFemales:
            female.setPreferenceList(generatePreferenceList(female, listOfMales))

        matches = {}
        for male in listOfMales:
            matches[male] = ''

        random.shuffle(listOfMales)

        # while there are free men
        while len(males_free) > 0:
            for male in listOfMales:
                for female in male.getPreferenceList():
                    if (male not in males_free):
                        break
                    if female not in list(matches.values()):
                        matches[male] = female
                        males_free.remove(male)
                        break
                    elif female in list(matches.values()):
                        current_suitor = list(matches.keys())[list(matches.values()).index(female)]
                        f_list = female.getPreferenceList()
                        # checking who is more preferred (should we do based on index or percentage?)
                        # if f_list.index(male) < f_list.index(current_suitor):
                        if generatePercentageOfSimilarAnswers(male, female) > generatePercentageOfSimilarAnswers(current_suitor, female):
                            matches[current_suitor] = ''
                            males_free.append(current_suitor)
                            matches[male] = female
                            males_free.remove(male)

        iterator = 1
        for male in matches.keys():
            responseStr += str(iterator) + ': {} ({}) + {} ({})\n'.format(male.getFullName(), male.getEmail(), matches[male].getFullName(), matches[male].getEmail())
            iterator += 1
    else:
        responseStr = "Groups are not equal!"

    return [responseStr, matches]

# this method will get all of the combinations and organize them in a single dictionary, then sort in descending order
def getMatches(formid, eventDate):
    parsedSubmissions = parseDataFromSubmissions(formid, eventDate)

    if parsedSubmissions == "ERROR_DATES":
        return "ERROR_DATES"
    else:
        matches = getStableMarriages(parsedSubmissions)
        return matches

def getOutputStringForFileSave(checkboxVal, response, eventDate):
    outputStr = ""
    if checkboxVal == "off":
        outputStr += "MATCHES FOR EVENT DATE: " + eventDate + "\n\n"
        outputStr += response[0]
    elif checkboxVal == "on":
        matches = response[1]
        iterator = 1
        for male in matches.keys():
            outputStr += "MATCHES FOR EVENT DATE: " + eventDate + " (With Preference Lists)\n\n"
            outputStr += 'MATCH {}: {} ({}) + {} ({})\n'.format(iterator, male.getFullName(), male.getEmail(), matches[male].getFullName(), matches[male].getEmail())
            
            outputStr += '{} Preferences: '.format(male.getFullName())
            for preference in male.getPreferenceList():
                outputStr += '[{} ({}%), '.format(preference.getFullName(), str(generatePercentageOfSimilarAnswers(male, preference)))
            outputStr = outputStr[:-2]
            outputStr += "]\n"

            outputStr += '{} Preferences: '.format(matches[male].getFullName())
            for preference in matches[male].getPreferenceList():
                outputStr += '[{} ({}%), '.format(preference.getFullName(), str(generatePercentageOfSimilarAnswers(matches[male], preference)))
            outputStr = outputStr[:-2]
            outputStr += "]\n"

            outputStr += "---------------------------"

    return outputStr


# gets submissions from json API class
def parseDataFromSubmissions(formId, dateOfEvent):
    submissions = jotform_api.JotformAPI.getFormSubmissions(formId)

    parsedSubmissions = []

    for sub in submissions:
        json_object = json.dumps(sub, indent=2) # converts to json and makes it pretty
        sub_json = json.loads(json_object) # makes json parsable

        # print(json_object)

        # submission data
        id = sub_json["id"]
        firstName = ""
        lastName = ""
        email = ""
        age = ""
        gender = ""
        responses = []
        responsesDict = {}
        creationDate = sub_json["created_at"]
        eventDate = ""

        for answer in sub_json["answers"]:

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
            elif sub_json["answers"][answer]["name"] == "eventDate":
                eventDate = sub_json["answers"][answer]["answer"]
            elif sub_json["answers"][answer]["name"] == "gender":
                try:
                    gender = sub_json["answers"][answer]["answer"]
                except:
                    gender = "NULL"

        # formattedEventDate = formatDate(eventDate)
        if eventDate == dateOfEvent:
            parsedSubmissions.append(submission.Submission(id, firstName, lastName, email, age, gender, responsesDict, creationDate, eventDate))
    if len(parsedSubmissions) == 0:
        return "ERROR_DATES"
    else:
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