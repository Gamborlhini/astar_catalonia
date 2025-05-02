import osmium
import csv

# filter based on objects with tags, coordinates, that are ways and have a maxspeed tag
fp = osmium.FileProcessor("../data/cataluna-latest.osm.pbf")\
        .with_filter(osmium.filter.EmptyTagFilter())\
        .with_locations()\
        .with_filter(osmium.filter.EntityFilter(osmium.osm.WAY))\
        .with_filter(osmium.filter.KeyFilter('maxspeed'))

nodes = []
edges = [[]]

# generate node and edges files
for obj in fp:
    for idx, node in enumerate(obj.nodes):
        # add to the nodes list in the format: ref #, latitude, longitude
        nodes.append([str(node.ref), node.lat, node.lon])
        # skip the first node (because we use i-1 indexing to create edges)
        if idx == 0:
            continue
        # append the previous node reference and current node reference as an edge
        # in the format: node 1, node 2, maxspeed
        edges.append([str(obj.nodes[idx - 1].ref), str(obj.nodes[idx].ref), obj.tags.get('maxspeed', '10')])

# write the nodes file
with open("../data/cataluna_nodes.csv", "w", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    for node in nodes:
        writer.writerow(node)

# write the edges file
with open("../data/cataluna_edges.csv", "w", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(edges)