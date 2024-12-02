import networkx as nx
from networkx.algorithms import community
from collections import Counter
import streamlit as st
from pyvis.network import Network
import matplotlib.pyplot as plt

# Load the graph from the GML file
file_path = "ingredients.gml"
graph = nx.read_gml(file_path)

# Centrality Measures
degree_centrality = nx.degree_centrality(graph)
closeness_centrality = nx.closeness_centrality(graph)
betweenness_centrality = nx.betweenness_centrality(graph)

top_3_degree = Counter(degree_centrality).most_common(3)
top_3_closeness = Counter(closeness_centrality).most_common(3)
top_3_betweenness = Counter(betweenness_centrality).most_common(3)

# Community detection
communities = community.greedy_modularity_communities(graph)
num_communities = len(communities)
community_sizes = [len(c) for c in communities]

st.subheader("Question 1 - Graph Overview")
# Create a Pyvis network
overview_net = Network(notebook=True, height="750px", width="100%", directed=False)
# Define layout for node positioning using NetworkX's spring layout
pos = nx.spring_layout(graph, seed=42)  # Seed ensures consistent layout
# Add nodes and edges manually to Pyvis with improved readability
color_palette = ["#33FF57", "#3357FF", "#FF5733"]
# Assign colors, positions, and node attributes
for idx, community_nodes in enumerate(communities):
    for node in community_nodes:
        # Assign node position from layout
        x, y = pos[node]
        overview_net.add_node(
            node,
            label=str(node),
            x=x * 800,  # Scale position for Pyvis
            y=y * 800,
            color=color_palette[idx % len(color_palette)],
            size=10 + (graph.degree[node] * 0.1),  # Adjust size based on degree
            font={"size": 14 + min(graph.degree[node], 10)},  # Adjust font size
        )
# Add edges
for edge in graph.edges():
    overview_net.add_edge(edge[0], edge[1], width=0.5)  # Thin edges for less clutter
# Disable physics for a static layout
overview_net.toggle_physics(False)
# Save and display the graph
overview_net.save_graph("overview_graph.html")
st.components.v1.html(overview_net.generate_html(), height=750)


st.subheader("Question 2 - Top 3 Ingredients by Centrality")
st.write("**Degree Centrality**:", top_3_degree)
st.write("**Closeness Centrality**:", top_3_closeness)
st.write("**Betweenness Centrality**:", top_3_betweenness)

st.subheader("Question 3 - Community Analysis")
st.subheader("Community Size Distribution")
plt.figure(figsize=(8, 6))
plt.bar(range(1, num_communities + 1), community_sizes, color="skyblue")
plt.xlabel("Community ID")
plt.ylabel("Size")
plt.title("Size of Each Community")
st.pyplot(plt)
st.write(f"**Number of Communities**: {num_communities}")
st.write(f"**Community Sizes**: {community_sizes}")

# Display members of the first communities
st.subheader("Members of First Community")
first_community_subgraph = graph.subgraph(communities[0])
net_first = Network(notebook=True, height="750px", width="100%")
net_first.from_nx(first_community_subgraph)
net_first.toggle_physics(False)
for node in first_community_subgraph.nodes():
    net_first.get_node(node)["color"] = "#33FF57"  # Highlight in green
net_first.save_graph("first_community.html")
st.components.v1.html(net_first.generate_html(), height=750)
first_community_members = sorted(list(communities[0]))
st.write(f"**Number of Members in First Community**: {len(first_community_members)}")
st.write("**Members (Example)**:", first_community_members[:10])

# Display members of the second communities
st.subheader("Members of Second Community")
second_community_subgraph = graph.subgraph(communities[1])
net_second = Network(notebook=True, height="750px", width="100%")
net_second.from_nx(second_community_subgraph)
net_second.toggle_physics(False)
for node in second_community_subgraph.nodes():
    net_second.get_node(node)["color"] = "#3357FF"  # Highlight in blue
net_second.save_graph("second_community.html")
st.components.v1.html(net_second.generate_html(), height=750)
second_community_members = sorted(list(communities[1]))
st.write(f"**Number of Members in Second Community**: {len(second_community_members)}")
st.write("**Members (Example)**:", second_community_members[:10])


# Add code for Third Community
st.subheader("Visualization of Third Community")
third_community_subgraph = graph.subgraph(communities[2])
net_third = Network(notebook=True, height="750px", width="100%")
net_third.from_nx(third_community_subgraph)
net_third.toggle_physics(False)
for node in third_community_subgraph.nodes():
    net_third.get_node(node)["color"] = "#FF5733"  # Highlight in red
net_third.save_graph("third_community.html")
st.components.v1.html(net_third.generate_html(), height=750)

third_community_members = sorted(list(communities[2]))
st.write(f"**Number of Members in Third Community**: {len(third_community_members)}")
st.write("**Members (Example)**:", third_community_members[:10])
