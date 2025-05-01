import numpy as np
import csv

def euclidian_distance(v1, v2):
    return np.linalg.norm(v1 - v2)

def coord_to_node(coordinates, nodes_file):
    nodes = []
    with open(nodes_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            nodes.append([row[1].strip(), row[2].strip()])

    closest_dist = np.inf
    closest_node = None
    for node in nodes:
        if dist := euclidian_distance([node[0], node[1]], coordinates) < closest_node:
            closest_node = node[0]
            closest_dist = dist
    return closest_node

