import matcher

class PairedSubmission:
    def __init__(self, male, female):
        self.male = male
        self.female = female

    def getNamesAsList(self):
        return [self.male.getFullName(), self.female.getFullName()]
    
    def getNamesAsString(self):
        return self.male.getFullName() + " & " + self.female.getFullName()
    
    def getPercentageOfSimilarAnswers(self):
        return matcher.getCompatibilityPercentage(self.male, self.female)
    
    def getMale(self):
        return self.male
    
    def getFemale(self):
        return self.female
        