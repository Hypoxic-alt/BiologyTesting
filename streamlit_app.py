import streamlit as st
import graphviz

st.title("5-Trophic Tier Energy Transfer Diagram")
st.write("This diagram illustrates the flow of energy from the Sun down to the Apex Predator.")

# Create a Graphviz Digraph
diagram = graphviz.Digraph(format='png')
diagram.attr(rankdir='TB')  # Set layout direction from Top to Bottom

# Define the nodes for each trophic tier
diagram.node("Sun", "Sun")
diagram.node("PP", "Primary Producer")
diagram.node("PC", "Primary Consumer")
diagram.node("SC", "Secondary Consumer")
diagram.node("AP", "Apex Predator")

# Create edges between nodes to represent energy transfer
diagram.edge("Sun", "PP", label="sunlight")
diagram.edge("PP", "PC", label="energy")
diagram.edge("PC", "SC", label="energy")
diagram.edge("SC", "AP", label="energy")

# Render the diagram in the Streamlit app
st.graphviz_chart(diagram)
