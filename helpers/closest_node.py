import numpy as np
import csv

# euclidian distance helper function
def euclidian_distance(v, t):
    return ((v[0]-t[0])** 2 + (v[1]-t[1]) ** 2) ** .5

# convert coordinates to the closest node
def coord_to_node(coordinates, nodes_file):
    nodes = []
    # read all the nodes into memory
    with open(nodes_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            nodes.append([str(row[0].strip()), float(row[1].strip()), float(row[2].strip())])

    # loop through every node to find the closest one
    # this is highly inefficient, a KD tree would be O(log(n)) as opposed to this O(n) implementation
    closest_dist = np.inf
    closest_node = None
    for node in nodes:
        if (dist := euclidian_distance([node[1], node[2]], coordinates)) < closest_dist:
            closest_node = node[0]
            closest_dist = dist
    # print and return the closest found node
    print("Closest node is: " + str(closest_node))
    return closest_node
