# README
## File Structure
```text
.
├── README.md
├── coordinate_run.py
├── data
│   ├── cataluna-latest.osm.pbf
│   ├── cataluna_edges.csv
│   ├── cataluna_nodes.csv
│   ├── monaco-latest.osm.pbf
│   ├── monaco_edges.csv
│   ├── monaco_nodes.csv
│   ├── sample_edges.csv
│   └── sample_nodes.csv
├── helpers
│   ├── Astar.py
│   ├── closest_node.py
│   ├── coord_appender.py
│   ├── generate_csv.py
│   └── visualization.py
├── main.py
└── output
    └── route.html
```
## Main Functions
### main.py
Launches an interactive terminal which allows you to select nodes and find the shortest travel time between them
Generates ./output/route.html visualization
### coordinate_run.py
Launches an interactive terminal to input source and destination coordinates to find the shortest travel time between
Generates ./output/route.html visualization

## Helper Functions
### Astar.py
Main implementation of the A* algorithm using heuristic reduced costs which satisfy the triangle inequality and \
Dijkstra's algorithm to find the shortest path between network nodes. 
### closest_node.py
Includes helper functions to find the closest node to a specified latitude and longitude
### coord_appender.py
Helper tool to append new nodes and undirected edges to the closest existing node
### generate_csv.py
Generates nodes and edges csv files from the input *.osm.pbf file
### visualization.py
Includes helper functions to visualize the route and discovered nodes using google maps api

