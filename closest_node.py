import Astar
import visualization
import numpy as np
import csv

def euclidian_distance(v, t):
    return ((v[0]-t[0])** 2 + (v[1]-t[1]) ** 2) ** .5

def coord_to_node(coordinates, nodes_file):
    nodes = []
    with open(nodes_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            nodes.append([str(row[0].strip()), float(row[1].strip()), float(row[2].strip())])

    closest_dist = np.inf
    closest_node = None
    for node in nodes:
        if (dist := euclidian_distance([node[1], node[2]], coordinates)) < closest_dist:
            closest_node = node[0]
            closest_dist = dist
    print("Closest node is: " + str(closest_node))
    return closest_node

if __name__ == '__main__':
    in_coordinates = [float(input("What is the starting latitude?\n")),float(input("What is the starting longitude?\n"))]
    dest_coordinates = [float(input("What is the destination latitude?\n")),float(input("What is the destination longitude?\n"))]
    graph = Astar.makeGraph_from_csv("cataluna_nodes.csv", "cataluna_edges.csv")
    time, dist, path, Found, predicesor, true_cost = Astar.Astar(graph, coord_to_node(in_coordinates, "cataluna_nodes.csv"), coord_to_node(dest_coordinates, "cataluna_nodes.csv"))
    print("Total time in minutes is: " + str(time * 60))
    print("Total distance in km is: " + str(dist))
    visualization.visualization(graph, path, Found, predicesor, true_cost)
