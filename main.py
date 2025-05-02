from helpers import Astar, visualization

print("Welcome to A-Star for Cataluña!")
print("Our most famous attractions are:")
print("Camp_Nou Sagrada_Familia Casa_Batllò Park_Güell Palace_Of_Catalan_Music Museu_Picasso La_Boqueria Casa_Mila La_Pedrera Santa_Maria_del_Mar")
print("But you can choose any where you want in the region")

start = input("Where do you want to start?\n")
end = input("Where do you want to go?\n")
# create the graph
graph = Astar.makeGraph_from_csv("data/cataluna_nodes.csv", "data/cataluna_edges.csv")

# run A* algorithm on the graph
time, dist, path, Found, predicesor, true_cost = Astar.Astar(graph,start,end)
print("Total time in minutes is: " + str(time * 60))
print("Total distance in km is: " + str(dist))
# visualize the graph with the final path and the discovered nodes
visualization.visualization(graph, path, Found, predicesor, true_cost)



