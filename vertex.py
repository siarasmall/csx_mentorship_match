from typing import List

class Vertex:
    """
    Vertex object for use as node in bipartite graph. Can represent mentor or mentee
    """
    def __init__(self, isMentor: bool, name: str, email: str, grade: str, classInterest: int, researchInterest: int, industryInterest: int, gradInterest: int, pivotInterest: int, groupsInterest: str, groups: List[str]):
        self.isMentor = isMentor
        self.name = name
        self.email = email
        self.grade = grade
        self.classInterest = classInterest
        self.researchInterest = researchInterest
        self.industryInterest = industryInterest
        self.gradInterest = gradInterest
        self.pivotInterest = pivotInterest
        self.groupsInterest = groupsInterest
        self.groups = groups
    
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

    def getGroupsInterest(self):
        return self.groupsInterest

    def getGroups(self) -> List[str]:
        return self.groups

    def display(self):
        print(f"Name: {self.name}, email: {self.email}, is mentor: {self.isMentor}, in group: {self.groupsInterest}, groups: {self.groups}")
    


