class Mentee:
    def __init__(self, name: str, email: str, grade: str, classInterest: int, researchInterest: int, industryInterest: int, gradInterest: int, pivotInterest: int):
        self.name = name
        self.email = email
        self.grade = grade
        self.classInterest = classInterest
        self.researchInterest = researchInterest
        self.industryInterest = industryInterest
        self.gradInterest = gradInterest
        self.pivotInterest = pivotInterest

    def getName(self):
        return self.name
    
    def getEmail(self):
        return self.email

    def getGrade(self):
        return self.grade
    
    def getClassInterest(self):
        return self.classInterest

    def getResearchInterest(self):
        return self.researchInterest

    def getIndustryInterest(self):
        return self.industryInterest

    def getGradInterest(self):
        return self.gradInterest

    def getPivotInterest(self):
        return self.pivotInterest
