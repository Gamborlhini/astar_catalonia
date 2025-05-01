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

def makeGraph(text):
    node_coords = {}
    edges = []
    weights = []

    parsing_edges = False

    with open(text, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                if "edges" in line.lower():
                    parsing_edges = True
                continue

            parts = line.split()

            if not parsing_edges:
                # Parse nodes: name x y
                name, x, y = parts
                node_coords[name] = (float(x), float(y))
            else:
                # Parse edges: source target weight
                src, tgt, weight = parts
                edges.append((src, tgt))
                weights.append(float(weight))

    # Build graph
    node_names = list(node_coords.keys())
    name_to_index = {name: i for i, name in enumerate(node_names)}
    indexed_edges = [(name_to_index[src], name_to_index[tgt]) for src, tgt in edges]
    coords = [node_coords[name] for name in node_names]

    g = Graph(directed=True)
    g.add_vertices(len(node_names))
    g.vs["name"] = node_names
    g.vs["coord"] = coords
    g.add_edges(indexed_edges)
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