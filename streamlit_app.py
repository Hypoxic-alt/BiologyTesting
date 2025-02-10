import streamlit as st
import graphviz

st.title("Vertical Energy Transfer Diagram with Losses & Efficiency")
st.markdown(
    """
This diagram illustrates the energy flow through trophic levels using an HTML table for each level.
Each trophic level shows:
- **Decomposition** losses (left cell)
- The **trophic level** and its **input energy** (center cell)
- **Respiration** losses (right cell)

Vertical edges show the transferred energy and trophic transfer efficiency.

**Example Values:**

- **Primary Producer:**  
  Input = 1000 J, Respiration = 600 J, Decomposition = 200 J  
  Transfer = 1000 − (600 + 200) = 200 J, Efficiency = 20%
  
- **Primary Consumer:**  
  Input = 200 J, Respiration = 120 J, Decomposition = 40 J  
  Transfer = 200 − (120 + 40) = 40 J, Efficiency = 20%
  
- **Secondary Consumer:**  
  Input = 40 J, Respiration = 24 J, Decomposition = 8 J  
  Transfer = 40 − (24 + 8) = 8 J, Efficiency = 20%
  
- **Apex Predator:**  
  Input = 8 J, Respiration = 4 J, Decomposition = 3 J  
  Transfer = 8 − (4 + 3) = 1 J, Efficiency ≈ 12.5%
    """
)

# Create a Graphviz Digraph with a top-to-bottom layout.
diagram = graphviz.Digraph(format='png')
diagram.attr(rankdir='TB')

# Define the Sun node (top of the diagram)
diagram.node("Sun", "Sun\n(1000 J)")

# Use HTML-like labels to create a table for each trophic level.
# The table has 3 columns: left (Decomposition), center (Main), right (Respiration).

# Primary Producer node
pp_label = '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>Decomposition<br/>200 J</TD>
    <TD>Primary Producer<br/>Input: 1000 J</TD>
    <TD>Respiration<br/>600 J</TD>
  </TR>
</TABLE>
>'''
diagram.node("PP", pp_label)

# Primary Consumer node
pc_label = '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>Decomposition<br/>40 J</TD>
    <TD>Primary Consumer<br/>Input: 200 J</TD>
    <TD>Respiration<br/>120 J</TD>
  </TR>
</TABLE>
>'''
diagram.node("PC", pc_label)

# Secondary Consumer node
sc_label = '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>Decomposition<br/>8 J</TD>
    <TD>Secondary Consumer<br/>Input: 40 J</TD>
    <TD>Respiration<br/>24 J</TD>
  </TR>
</TABLE>
>'''
diagram.node("SC", sc_label)

# Apex Predator node
ap_label = '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>Decomposition<br/>3 J</TD>
    <TD>Apex Predator<br/>Input: 8 J</TD>
    <TD>Respiration<br/>4 J</TD>
  </TR>
</TABLE>
>'''
diagram.node("AP", ap_label)

# Now add vertical edges between nodes.
diagram.edge("Sun", "PP", label="1000 J from sunlight")
diagram.edge("PP", "PC", label="Transfer: 200 J\nEfficiency: 20%")
diagram.edge("PC", "SC", label="Transfer: 40 J\nEfficiency: 20%")
diagram.edge("SC", "AP", label="Transfer: 8 J\nEfficiency: 20%")

# Optionally, show net energy and efficiency for Apex Predator (since it does not transfer further)
diagram.node("AP_net", "Net Energy: 1 J\nEfficiency: 12.5%")
diagram.edge("AP", "AP_net", style="dotted", arrowhead="none")

st.graphviz_chart(diagram)
