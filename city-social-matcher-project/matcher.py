import operator
import jotform_api

# define Person class, this will be used for each responder to the form
class Person:
    def __init__(self, name, responses, phone, email):
        self.name = name
        self.responses = responses
        self.phone = phone
        self.email = email

    def getName(self):
        return self.name
    
    def getResponses(self):
        return self.responses
    
    def getPhone(self):
        return self.phone
    
    def getEmail(self):
        return self.email
    
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

    return (sum(percentages) / len(percentages)) * 100 # get the average percentage and move it one decimal

# this method will get all of the combinations and organize them in a single dictionary, then sort in descending order
def getMatches():
    # adding combinations and scores to dictionary
    i = 0
    for female in females:
        for male in males:
            responsesDict[male.getName() + " + " + female.getName()] = str(getCompatibilityPercentage(male, female)) + "%"

    sorted_responsesDict = dict( sorted(responsesDict.items(), key=operator.itemgetter(1), reverse=True)) # reverse=True sorts in descending
    # print(sorted_responsesDict)
    return sorted_responsesDict


def getSubmissions(formId):
    responses = jotform_api.JotformAPI.getResponses(formId)
    # print(responses)
    return responses


# --- sample input ---
responses = [0, 1, 2, 3, 4]

responsesDict = {

}

pAdam = Person("Adam", [responses[0], responses[4], responses[2], responses[2], responses[3]], 4405552222, "adamanderson@test.com")
pBill = Person("Bill", [responses[2], responses[2], responses[1], responses[3], responses[4]], 4405551234, "billwilly@test.com")
pCarl = Person("Carl", [responses[0], responses[4], responses[2], responses[2], responses[3]], 4405554321, "carlcarter@test.com")
pDan = Person("Dan", [responses[1], responses[2], responses[3], responses[3], responses[1]], 4405555543, "dandonaldson@test.com")

pAlly = Person("Ally", [responses[4], responses[3], responses[3], responses[0], responses[2]], 4405552814, "allyarlington@test.com")
pBeth = Person("Beth", [responses[2], responses[2], responses[3], responses[3], responses[1]], 4405558053, "bethbarry@test.com")
pCait = Person("Cait", [responses[0], responses[2], responses[1], responses[1], responses[2]], 4405550932, "caitcarrington@test.com")
pDina = Person("Dina", [responses[2], responses[3], responses[2], responses[2], responses[0]], 4405559021, "dinadomino@test.com")

males = [pAdam, pBill, pCarl, pDan]
females = [pAlly, pBeth, pCait, pDina]