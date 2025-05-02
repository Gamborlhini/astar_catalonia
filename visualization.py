import requests
import polyline
from urllib.parse import quote_plus

def visualization(Graph, path, Found,predicesor, true_cost):
    route = build_route_from_path(Graph, path)
    from gmplot import GoogleMapPlotter

    # Center the map at the first point
    start_lat, start_lng = route[0]

    gmap = GoogleMapPlotter(start_lat, start_lng, zoom=14, apikey="AIzaSyA3BHlhNoO2e6w4URB8aCf5Orc1A4Rcw7s")

    # Unzip to two lists: lats, lngs
    lats, lngs = zip(*route)

    # Draw the route as a red line of width 3
    gmap.plot(lats, lngs, color='red', edge_width=3)

    # Optionally put markers at each waypoint
    gmap.scatter(lats, lngs, color='blue', size=20, marker=True)

    plotted = set(path)
    while any(v not in plotted for v in Found):
        candidates = [v for v in Found if v not in plotted]
        furthest  = max(candidates, key=lambda v: true_cost[v])

        subpath = reconstruct_path(predicesor, furthest)
        subroute = build_route_from_path(Graph, subpath)
        sublats, sublngs = zip(*subroute)

        gmap.plot(sublats, sublngs, color='purple', edge_width=3)

        # <-- use update (or .add for a single node) on your set:
        plotted.update(subpath)


    # Write out an HTML file you can open in your browser
    gmap.draw("route.html")
    print("Open route.html in your browser to see the map.")
    return 

def build_route_from_path(graph, path):
    route = []
    for node_name in path:
        vertex = graph.vs.find(name=node_name)
        lon, lat = vertex["coord"]
        route.append((lat, lon))  # convert to (lat, lon)
    return route

def reconstruct_path(predicesor, end):
    path = []
    while end is not None:
        path.append(end)
        end = predicesor[end]
    return path[::-1]  # reverse