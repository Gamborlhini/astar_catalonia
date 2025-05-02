from helpers import Astar, visualization, closest_node
if __name__ == '__main__':
    # input source and destination coordinates
    in_coordinates = [float(input("What is the starting latitude?\n")),float(input("What is the starting longitude?\n"))]
    dest_coordinates = [float(input("What is the destination latitude?\n")),float(input("What is the destination longitude?\n"))]
    # create the graph from the files
    graph = Astar.makeGraph_from_csv("cataluna_nodes.csv", "cataluna_edges.csv")
    # runs A* using the closest nodes to the inputted coordinates
    time, dist, path, Found, predicesor, true_cost = Astar.Astar(graph,
                                                                 closest_node.coord_to_node(in_coordinates, "data/cataluna_nodes.csv"),
                                                                 closest_node.coord_to_node(dest_coordinates, "data/cataluna_nodes.csv"))
    # print metrics
    print("Total time in minutes is: " + str(time * 60))
    print("Total distance in km is: " + str(dist))

    # visualize result
    visualization.visualization(graph, path, Found, predicesor, true_cost)