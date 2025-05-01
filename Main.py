import Astar 

print("Welcome to A-Star")
start = input("Where do you want to start?\n")
end = input("Where do you want to go?\n")
graph = Astar.makeGraph_from_csv("cataluna_nodes.csv", "cataluna_edges.csv")
print(Astar.Astar(graph,start,end))

