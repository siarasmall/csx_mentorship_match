import csv
import statistics
import re
import argparse
from bipartite_graph import BipartiteGraph 
from vertex import Vertex 

NUM_PREFERENCES = 4
# Sets bias towards similar groups for when there is a prefence for shared identity- can scale up/down 
# depending on how important we think this is
GROUP_BIAS = 0.2
# Verbosity for debugging/ printing matches
VERBOSE = True

def calcCompatibility(mentor: Vertex, mentee: Vertex) -> float:
    """
    Calculates the compatibility between a mentor and a mentee. 
    Returns a float from 0 - 1 representing compatibility
    """

    # Adjustment for marginalized groups preference
    prefAdjustment = 0

    # Case in which there is inherent incompatibility -> compatibility is 0
    if ((mentor.getGroupsInterest() == "Yes" and mentee.getGroupsInterest() == "No") or (mentor.getGroupsInterest() == "No" and mentee.getGroupsInterest() == "Yes")): 
        return 0

    # Case in which preferences are taken into account
    if (mentor.getGroupsInterest() == "Preferably" or mentee.getGroupsInterest() == "Preferably" or 
        mentor.getGroupsInterest() == "Yes" or mentee.getGroupsInterest() == "Yes"):

        # Get num of similarities between groups 
        similarities = len([group for group in mentee.getGroups() if group in mentor.getGroups() and group])
        prefAdjustment = similarities * GROUP_BIAS

    # Calculates compatibility of interests. Standardization: float from 0-1, 0 being the least compatible and 1 the most.
    mentorPrefs = [mentor.getClassInterest(), mentor.getGradInterest(), mentor.getIndustryInterest(), mentor.getPivotInterest(), mentor.getResearchInterest()]
    menteePrefs = [mentee.getClassInterest(), mentee.getGradInterest(), mentee.getIndustryInterest(), mentee.getPivotInterest(), mentee.getResearchInterest()]
    normalizedDiffs = []

    # Algo: difference of preferences, normalized by dividing by num of preferences, averaged
    for i in range(NUM_PREFERENCES):
        normalizedDiffs.append(1 - (abs(float(mentorPrefs[i]) - float(menteePrefs[i])) / NUM_PREFERENCES))

    # Avgd and takes preference bias into account
    prelim = statistics.mean(normalizedDiffs) + prefAdjustment

    # Thresholds at a max of 1
    return (prelim if prelim <= 1 else 1)

def main():
    # Init bipartite graph 
    graph = BipartiteGraph()

    # Get .csv filename from command line
    parser = argparse.ArgumentParser(description = 'CSX Mentor-Mentee Matching Program')
    parser.add_argument('input_file', type = str, help = 'Path to the input CSV file containing mentor and mentee data')

    args = parser.parse_args()
    inputFile = args.input_file

    # Read in data from csv, make vertices for each row, insert each vertex into graph
    with open(inputFile, 'r') as file:
        # Skip header row
        next(file)  

        reader = csv.reader(file, delimiter=',', quotechar='"')

        # Read each row and store data in Vertex object
        for row in reader:
            isMentor = row[4].split()[0] == 'Mentor'
            capacity = 3 if row[12] == 'Yes' else 1
            groups = []

            # YesYes check is bandaid solution lol
            # Adds groups to list of groups
            if (row[10] != "No" and row[11] != 'YesYes'):
                groups = re.split(',', row[11])
                groups = [group.replace("'", "").strip() for group in groups]
            # This approach assumes there will never be more mentors than mentees. Reasonable assumption based on 
            # past years but should probably change this at some point. 

            if isMentor:
                for i in range(capacity):
                    # Create Mentor vertex. Append copy number to name (allows for mentor to be matched with multiple mentees)
                    newVertex = Vertex(
                        isMentor = isMentor, name = f"{row[1]} copy{i + 1}", email = row[2],
                        grade = row[3], classInterest = row[5], researchInterest = row[6],
                        industryInterest = row[7], gradInterest = row[8],
                        pivotInterest = row[9], groupsInterest = row[10], groups = groups
                    )
                    graph.addVertex(newVertex, 'Mentor')
            else:
                # Create Mentee vertex
                newVertex = Vertex(
                    isMentor = isMentor, name = row[1], email = row[2], grade = row[3],
                    classInterest = row[5], researchInterest = row[6], industryInterest = row[7],
                    gradInterest = row[8], pivotInterest = row[9], groupsInterest = row[10], groups = groups
                )
                graph.addVertex(newVertex, 'Mentee')

    # Preserve original mentor set
    mentors = graph.getMentors()
    mentees = graph.getMentees()

    # Adds edges to graphrepresenting compatibility btwn all mentors/mentees
    for mentor in mentors:
        for mentee in mentees:
            score = calcCompatibility(mentor, mentee)
            graph.addEdge(mentor, mentee, score)

    # Generate match pairings 
    matching = graph.genMatches()

    # Output match data to .csv. Will overwrite anything in matchings.csv!!!
    with open('matchings.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
        
        # Write header row
        spamwriter.writerow(['Mentor name', 'Mentee name', 'Mentor email', 'Mentee email', 'Mentor grade', 'Mentee grade', 
                            'Mentor class interest', 'Mentee class interest', 'Mentor research interest', 
                            'Mentee research interest', 'Mentor industry interest', 'Mentee industry interest', 
                            'Mentor grad school interest', 'Mentee grad school interest', 'Mentor major pivot interest', 
                            'Mentee major pivot interest'])
        
        # Matching pairs are unordered- determine who is mentee, mentor
        for a, b in matching:
            if a.isMentor: 
                mentor = a
                mentee = b
            else: 
                mentor = b
                mentee = a

            # Write data
            spamwriter.writerow([
                mentor.getName(), mentee.getName(), mentor.getEmail(), mentee.getEmail(), 
                mentor.getGrade(), mentee.getGrade(), mentor.getClassInterest(), mentee.getClassInterest(), 
                mentor.getResearchInterest(), mentee.getResearchInterest(), mentor.getIndustryInterest(), 
                mentee.getIndustryInterest(), mentor.getGradInterest(), mentee.getGradInterest(), 
                mentor.getPivotInterest(), mentee.getPivotInterest()
            ])
            
            if VERBOSE:
                print(f"Mentor: {mentor.name} (Email: {mentor.email}) is matched with Mentee: {mentee.name} (Email: {mentee.email})")
                print(f"Compatibility score: {graph.getEdge(mentor, mentee)}")
  
            
if __name__ == '__main__':
    main()