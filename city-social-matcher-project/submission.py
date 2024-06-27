class Submission:
    def __init__(self, firstName, lastName, email, age, gender, responses, creationDate):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.age = age
        self.gender = gender
        self.responses = responses
        self.creationDate = creationDate


    def getFirstName(self):
        return self.firstName
    
    def getLastName(self):
        return self.lastName
    
    def getFullName(self):
        return self.firstName + " " + self.lastName
    
    def getEmail(self):
        return self.email
    
    def getAge(self):
        return self.age
    
    def getGender(self):
        return self.gender
    
    def getResponses(self):
        return self.responses