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
            path = reconstruct_path(predicesor, end)
            print(" → ".join(path))
            total_weight = sum_edge_weights(graph, path)
            total_dist = sum_edge_dist(graph, path)
            return total_weight, total_dist, path, Found, predicesor, true_cost
        
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
    print("NO PATH WAS FOUND")




def h_reduced_length(edge, a, b, t) :
    return (edge["weight"]) - h(a,t)/120 + h(b,t)/120

def euclidianDist(v, t):
    return ((v["coord"][0]-t["coord"][0])** 2 + (v["coord"][1]-t["coord"][1]) ** 2) ** .5


def h(v, t):
    lon1 = v["coord"][0]
    lat1 = v["coord"][1]
    lon2 = t["coord"][0]
    lat2 = t["coord"][1]
    return haversine_np(lon1, lat1, lon2, lat2)

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
            if len(row) != 3:
                continue
            src, tgt, speed = row[0].strip(), row[1].strip(), row[2].strip()
            
            speed = parse_speed(speed)
            if src in node_coords and tgt in node_coords:
                edges.append((name_to_index[src], name_to_index[tgt]))
                x1, y1 = node_coords[src]
                x2, y2 = node_coords[tgt]
                dist = haversine_np(x1,y1,x2,y2) / int (speed)
                weights.append(dist)

    # Build the graph
    g = Graph(directed=True)
    g.add_vertices(len(node_names))
    g.vs["name"] = node_names
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


def parse_speed(speed_str):
    try:
        return int(speed_str)
    except ValueError:
        return speed_limit(speed_str)
    
def speed_limit(code):
    speed_defaults = {
        "ES:urban": 50,
        "ES:rural": 90,
        "ES:motorway": 120
    }
    return speed_defaults.get(code, 50)  # default = 50

def sum_edge_weights(graph, path):
    total = 0
    for i in range(len(path) - 1):
        source = graph.vs.find(name=path[i]).index
        target = graph.vs.find(name=path[i+1]).index
        edge = graph.get_eid(source, target)
        total += graph.es[edge]["weight"]
    return total

def sum_edge_dist(graph, path):
    total = 0
    for i in range(len(path) - 1):
        source = graph.vs.find(name=path[i])
        target = graph.vs.find(name=path[i+1])
        total += h(source, target)
    return total

def reconstruct_path(predicesor, end):
    path = []
    while end is not None:
        path.append(end)
        end = predicesor[end]
    return path[::-1]  # reverse

def haversine_np(lon1, lat1, lon2, lat2):
    import math
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    Reference:
        https://stackoverflow.com/a/29546836/7657658
    """
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(
        dlat / 2.0)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2.0)**2

    c = 2 * math.asin(math.sqrt(a))
    km = 6371 * c
    return km