from igraph import Graph
from heapdict import heapdict

#Input is Network of vertices and edges, where the vertices have euclidian coord
# and the edges have weights. Also have input of start and end nodes.
#Output is shortest path dist, while printing the path
def Astar(graph, start, end):
    #Initialize found nodes and distance of each node from start
    Found = []
    dd = heapdict()
    # True-costs (initialize all to infinity except for start)
    true_cost = {v["name"]: float("inf") for v in graph.vs}
    true_cost[start] = 0

    # Make a min heap starting with start vertex
    dd[start] = h(graph.vs.find(name=start), graph.vs.find(name=end)) 

    #Initialize predicesor function
    predicesor = {}
    for vertex in graph.vs:
        predicesor[vertex["name"]] = None

    # main loop of Astar, the "lets make a deal sectio"
    while any(v not in Found and dd[v] < float("inf") for v in dd):
        #selects the argmin v in dd that has not been found yet
        v, v_dist = dd.popitem()
        #puts v in found
        Found.append(v)

        #checks if it is our target, and if so returns, and prints path
        if v == end:
            print_path(end, predicesor, end)
            return true_cost[end]  
        
        # gets a list of all incident edges of the v we found
        v_index = graph.vs.find(name=v).index
        edge_ids = graph.incident(v_index, mode="OUT")
        
        # iterates through all, and will update distance of which, using the reduced h heuristic
        for eid in edge_ids:
            edge = graph.es[eid]
            w = graph.vs[edge.target]["name"]
            if w not in Found:
                v_vertex = graph.vs.find(name=v)
                end_vertex = graph.vs.find(name=end)
                w_vertex = graph.vs.find(name=w)
                if true_cost[v] + h_reduced_length(edge,v_vertex,w_vertex,end_vertex) < true_cost[w]:
                    true_cost[w] = true_cost[v] + h_reduced_length(edge,v_vertex,w_vertex,end_vertex)
                    dd[w] = true_cost[v] + h_reduced_length(edge,v_vertex,w_vertex,end_vertex)
                    predicesor[w] = v
    return dd[end]




def h_reduced_length(edge, a, b, t) :
    return edge["weight"] - h(a,t) + h(b,t)

def h(v, t):
    return ((v["coord"][0]-t["coord"][0])** 2 + (v["coord"][1]-t["coord"][1]) ** 2) ** .5

def makeGraph_from_csv(nodes_file, edges_file):
    import csv
    import math
    from igraph import Graph

    node_coords = {}
    edges = []
    weights = []

    # Load node coordinates
    with open(nodes_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 3:
                continue
            node_id, lat, lon = row
            node_coords[node_id] = (float(lon), float(lat))  # x=lon, y=lat

    # Map node IDs to graph vertex indices
    node_names = list(node_coords.keys())
    name_to_index = {name: i for i, name in enumerate(node_names)}
    coords = [node_coords[name] for name in node_names]

    # Load edges and compute weights
    with open(edges_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 2:
                continue
            src, tgt = row[0].strip(), row[1].strip()
            if src in node_coords and tgt in node_coords:
                edges.append((name_to_index[src], name_to_index[tgt]))
                x1, y1 = node_coords[src]
                x2, y2 = node_coords[tgt]
                dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                weights.append(dist)

    # Build the graph
    g = Graph(directed=True)
    g.add_vertices(len(node_names))
    g.vs["name"] = str (node_names)
    g.vs["coord"] = coords
    g.add_edges(edges)
    g.es["weight"] = weights

    return g

def print_path(end, predicesor, final):
        v = predicesor[end]
        if v != None:
            print_path(v, predicesor, final)
        if end != final:
            print(end + "--->")
        else:
            print(end)