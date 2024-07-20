import matcher

class SubmissionPair:
    def __init__(self, male, female):
        self.male = male
        self.female = female

    def getNamesAsList(self):
        return [self.male.getFullName(), self.female.getFullName()]
    
    def getNamesAsString(self):
        return self.male.getFullName() + " & " + self.female.getFullName()
    
    def getPercentageOfSimilarAnswers(self):
        maleResp = self.male.getResponses()
        femaleResp = self.female.getResponses()

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
    
    def getMale(self):
        return self.male
    
    def getFemale(self):
        return self.female
        