from igraph import Graph
from heapdict import heapdict

def Astar(graph, start, end):
    Found = []
    dd = heapdict()
    for vertex in graph.vs:
        if vertex["name"] != start:
            dd[vertex["name"]] = float("inf")
    dd[start] = 0

    predicesor = {}
    for vertex in graph.vs:
        predicesor[vertex] = None

    while any(v not in Found and dd[v] < float("inf") for v in dd):
        v, v_dist = dd.popitem()
        Found.append(v)

        if v == end:
            return v_dist  
        
        v_index = graph.vs.find(name=v).index
        edge_ids = graph.incident(v_index, mode="OUT")
        for eid in edge_ids:
            edge = graph.es[eid]
            w = graph.vs[edge.target]["name"]
            if w not in Found:
                if v_dist + edge["weight"] < dd[w]:
                    dd[w] = v_dist + edge["weight"]
                    predicesor[w] = v
    
    return dd[end]




def h_reduced_length(edge) :
    return 

def h():
    return

def makeGraph(text):
    edges = []
    weights = []

    with open(text, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                source, target, weight = parts
                edges.append((source, target))
                weights.append(float(weight))

    # Step 2: Extract unique node names
    node_names = list(set([n for edge in edges for n in edge]))

    # Step 3: Map node names to integer indices (igraph uses integers)
    name_to_index = {name: i for i, name in enumerate(node_names)}
    indexed_edges = [(name_to_index[src], name_to_index[dst]) for src, dst in edges]

    # Step 4: Create the graph
    g = Graph(directed=True)
    g.add_vertices(len(node_names))
    g.vs["name"] = node_names
    g.add_edges(indexed_edges)
    g.es["weight"] = weights
    
    return g