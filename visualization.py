import requests
import polyline
from urllib.parse import quote_plus

def visualization(Graph, path):
    route = build_route_from_path(Graph, path)
    encoded = polyline.encode(route)

    params = {
    'size': '640x480',
    'maptype': 'roadmap',
    # draw a blue, 5-px wide line following the encoded route:
    'path': f"enc:{encoded}|color:0x0000ff|weight:5",
    'key': 'AIzaSyA3BHlhNoO2e6w4URB8aCf5Orc1A4Rcw7s'
    }
    
    url = (
    "https://maps.googleapis.com/maps/api/staticmap?"
    + "&".join(f"{k}={quote_plus(v)}" for k, v in params.items())
    )

    resp = requests.get(url)
    resp.raise_for_status()
    with open("route_map.png", "wb") as f:
        f.write(resp.content)

    print("Saved route_map.png")
    return 

def build_route_from_path(graph, path):
    route = []
    for node_name in path:
        vertex = graph.vs.find(name=node_name)
        lon, lat = vertex["coord"]
        route.append((lat, lon))  # convert to (lat, lon)
    return route