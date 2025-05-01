import Astar 

print("Welcome to A-Star")
start = input("Where do you want to start?\n")
end = input("Where do you want to go?\n")
graph = Astar.makeGraph_from_csv("sample_nodes.csv", "sample_edges.csv")
print(graph.vs["name"])
time, dist = Astar.Astar(graph,start,end)
print("Total time is: " + str(time))
print("Total distance is: " + str(dist))

