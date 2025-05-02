import Astar 
import visualization

print("Welcome to A-Star for Cataluña!")
print("Our most famous attractions are:")
print("Camp_Nou Sagrada_Familia Casa_Batllò Park_Güell Palace_Of_Catalan_Music")
print("But you can choose any where you want in the region")

start = input("Where do you want to start?\n")
end = input("Where do you want to go?\n")
graph = Astar.makeGraph_from_csv("cataluna_nodes.csv", "cataluna_edges.csv")
print(graph.vs["name"])

time, dist, path, Found, predicesor, true_cost = Astar.Astar(graph,start,end)
print("Total time in minutes is: " + str(time * 60))
print("Total distance in km is: " + str(dist))
visualization.visualization(graph, path, Found, predicesor, true_cost)



