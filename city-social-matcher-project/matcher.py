import operator
import jotform_api
import json
import submission
import submission_pair
import random
    
# TODO --
# remove generatePercentage from submission_pair class
# maybe remove submission_pair class
# put in checks to make sure lists are equal
# put in more info for the user
# define methods
# this method will combine each persons answers to see how similar they are, and give it a percentage of similarity
def generatePercentageOfSimilarAnswers(male, female):
        maleResp = male.getResponses()
        femaleResp = female.getResponses()

        percentages = []

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

def generatePreferenceList(submission, suitors):
    pairs = []
    pairsDict = {}
    preferenceList = []

    if submission.getGender() == "Male":
        for suitor in suitors:
            pairs.append(submission_pair.SubmissionPair(submission, suitor))

        for pair in pairs:
            pairsDict[pair] = str(pair.getPercentageOfSimilarAnswers()) + "%"

        pairsDict_sorted_desc = dict( sorted(pairsDict.items(), key=operator.itemgetter(1), reverse=True))

        for key in pairsDict_sorted_desc:
            preferenceList.append(key.getFemale())

    elif submission.getGender() == "Female":
        for suitor in suitors:
            pairs.append(submission_pair.SubmissionPair(suitor, submission))

        for pair in pairs:
            pairsDict[pair] = str(pair.getPercentageOfSimilarAnswers()) + "%"

        pairsDict_sorted_desc = dict( sorted(pairsDict.items(), key=operator.itemgetter(1), reverse=True))

        for key in pairsDict_sorted_desc:
            preferenceList.append(key.getMale())

    return preferenceList

def getStableMarriages(formid):
    parsedSubmissions = parseDataFromSubmissions(formid)

    listOfMales = []
    listOfFemales = []

    for sub in parsedSubmissions:
        if sub.getGender() == "Male":
            listOfMales.append(sub)
        elif sub.getGender() == "Female":
            listOfFemales.append(sub)

    males_free = list(listOfMales)
    females_free = list(listOfFemales)
    
    # get preference lists for each male and female
    for male in listOfMales:
        male.setPreferenceList(generatePreferenceList(male, listOfFemales))

    for female in listOfFemales:
        female.setPreferenceList(generatePreferenceList(female, listOfMales))

    # for male in listOfMales:
    #     print(male.getFullName() + " PREFS: \n")
    #     for female in male.getPreferenceList():
    #         print(female.getFullName() + " " + str(generatePercentageOfSimilarAnswers(male, female)) + "%")
    #     print("\n")
    # for female in listOfFemales:
    #     print(female.getFullName() + " PREFS: \n")
    #     for male in female.getPreferenceList():
    #         print(male.getFullName() + " " + str(generatePercentageOfSimilarAnswers(male, female)) + "%")
    #     print("\n")

    matches = {}
    for male in listOfMales:
        matches[male] = ''

    random.shuffle(listOfMales)

    while len(males_free) > 0:
        for male in listOfMales:
            print("PROCESSING MALE: " + male.getFullName())
            for female in male.getPreferenceList():
                if (male not in males_free):
                    print("MALE ALREADY MATCHED, NEXT!")
                    break
                print("\nFREE MALES: \n")
                for item in males_free:
                    print(item.getFullName() + " (" + item.getId() + ")")
                print("\n")
                print(male.getFullName() + "'s Top Choice: " + female.getFullName())
                if female not in list(matches.values()):
                    print(male.getFullName() + " AND " + female.getFullName() + " ARE MATCHED")
                    matches[male] = female
                    males_free.remove(male)
                    break
                elif female in list(matches.values()):
                    current_suitor = list(matches.keys())[list(matches.values()).index(female)]
                    print(female.getFullName() + " ALREADY MATCHED WITH " + current_suitor.getFullName())
                    f_list = female.getPreferenceList()
                    # checking who is more preferred (should we do based on index or percentage?)
                    # if f_list.index(male) < f_list.index(current_suitor):
                    if generatePercentageOfSimilarAnswers(male, female) > generatePercentageOfSimilarAnswers(current_suitor, female):
                        matches[current_suitor] = ''
                        males_free.append(current_suitor)
                        matches[male] = female
                        males_free.remove(male)
                        print('{} was earlier engaged to {} but now is engaged to {}! '.format(female.getFullName(), current_suitor.getFullName(), male.getFullName()))







    print('\n \n \n ')
    print('Stable Matching Finished ! Happy engagement !')
    for male in matches.keys():
        print('{} is engaged to {} !'.format(male.getFullName(), matches[male].getFullName()))

# this method will get all of the combinations and organize them in a single dictionary, then sort in descending order
def getMatches(formid):
    getStableMarriages(formid)
    parsedSubmissions = parseDataFromSubmissions(formid)

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
            possibleMatches.append(submission_pair.SubmissionPair(male, female))

    # for every possible match, store it in a dictionary with itself as the key and the compatibility percentage as the value
    # (this is so we can sort it from highest to lowest percentage
    for match in possibleMatches:
        matchesDict[match] = str(match.getPercentageOfSimilarAnswers()) + "%"

    # sorts the dictionary from highest to lowest value
    sorted_matchesDict = dict( sorted(matchesDict.items(), key=operator.itemgetter(1), reverse=True))

    uniqueMatchesDict = { }
    matchedFemales = []
    matchedMales = []

    for key in sorted_matchesDict:
        # going from highest percentage to lowest, if a male or female has already been matched, then skip, otherwise they are matched
        if key.getFemale() not in matchedFemales and key.getMale() not in matchedMales:
            uniqueMatchesDict[key] = sorted_matchesDict[key]
            matchedFemales.append(key.getFemale()) # add female to list of matched females
            matchedMales.append(key.getMale()) # add male to list of matched males

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
        id = sub_json["id"]
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
        parsedSubmissions.append(submission.Submission(id, firstName, lastName, email, age, gender, responsesDict, creationDate))

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