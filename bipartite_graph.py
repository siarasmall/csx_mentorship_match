from vertex import Vertex
import networkx as nx

class BipartiteGraph:
    def __init__(self):
        self.mentors = []  
        self.mentees = []  
        self.adjList = {}  # Adjacency list to store edges with weights

    def addVertex(self, node: Vertex, type: str):
        if type == 'Mentor':
            self.mentors.append(node)
        elif type == 'Mentee':
            self.mentees.append(node)
        else:
            raise ValueError("type must be either 'Mentor' or 'Mentee'")
        self.adjList[node] = []

    def addEdge(self, u: Vertex, v: Vertex, weight: float):
        if ((u in self.mentors and v in self.mentees) or (u in self.mentees and v in self.mentors)):
            # Add mentee and weight to mentor's list
            self.adjList[u].append((v, weight))
            # Add mentor and weight to mentee's list
            self.adjList[v].append((u, weight)) 
        else:
            raise ValueError("Trying to connect two from the same set")

    def display(self):
        print("Mentor set:")
        for node in self.mentors:
            matches = [(n.name, w) for n, w in self.adjList[node]]
            print(f"{node.name} (Capacity: {node.capacity}, Matches: {matches})")

        print("Mentee set:")
        for node in self.mentees:
            matches = [(n.name, w) for n, w in self.adjList[node]]
            print(f"{node.name} (Capacity: {node.capacity}, Matches: {matches})")

    def getMentors(self):
        return self.mentors

    def getNumMentors(self):
        return len(self.mentors)

    def getMentees(self):
        return self.mentees

    def getNumMentees(self):
        return len(self.mentees)

    def getAdjList(self, mentor):
        return self.adjList[mentor]

    def getEdge(self, mentor: Vertex, mentee: Vertex):
        edges = self.adjList[mentor]
        for edge in edges:
            if edge[0].getName() == mentee.getName():
                return edge[1]
        return -1
    
    def genMatches(self):
        # Create a bipartite graph using networkx
        G = nx.Graph()

        # Add mentor and mentee nodes to the graph
        G.add_nodes_from(self.mentors, bipartite=0)
        G.add_nodes_from(self.mentees, bipartite=1)

        # Add edges between mentors and mentees with negative compatibility score as weight
        for mentor in self.mentors:
            for mentee, weight in self.adjList[mentor]:
                G.add_edge(mentor, mentee, weight = -weight)

        # Find the maximum weight matching with Vertex objects preserved
        matching = nx.algorithms.matching.max_weight_matching(G, maxcardinality=True, weight='weight')
        return matching

