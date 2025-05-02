import csv
import closest_node

nodes = [
    ["Museu_Picasso", 41.3853993358149, 2.181000849111881],
    ["La_Boqueria", 41.38175407367943, 2.171584890492097],
    ["Casa_Mila", 41.39542470126962, 2.161913136755619],
    ["La_Pedrera", 41.39542470126962, 2.161913136755619],
    ["Santa_Maria_del_Mar", 41.384007791350356, 2.182006730968819]
]
edges = [[]]

for node in nodes:
    print(node)
    closest = closest_node.coord_to_node([node[1], node[2]], "cataluna_nodes.csv")
    edges.append([closest, node[0], 30])
    edges.append([node[0], closest, 30])

with open('cataluna_nodes.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(nodes)

with open('cataluna_edges.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(edges)