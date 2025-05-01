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
        predicesor[vertex["name"]] = None

    while any(v not in Found and dd[v] < float("inf") for v in dd):
        v, v_dist = dd.popitem()
        Found.append(v)

        if v == end:
            print_path(end, predicesor, end)
            return v_dist  
        
        v_index = graph.vs.find(name=v).index
        edge_ids = graph.incident(v_index, mode="OUT")
        for eid in edge_ids:
            edge = graph.es[eid]
            w = graph.vs[edge.target]["name"]
            if w not in Found:
                if v_dist + h_reduced_length(edge,graph.vs.find(name=v),graph.vs.find(name=w),graph.vs.find(name=end)) < dd[w]:
                    dd[w] = v_dist + h_reduced_length(edge,graph.vs.find(name=v),graph.vs.find(name=w),graph.vs.find(name=end))
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