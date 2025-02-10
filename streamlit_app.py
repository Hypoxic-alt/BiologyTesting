import streamlit as st
import graphviz

st.title("Energy Transfer with Losses Diagram")
st.write(
    """
    This diagram illustrates the flow of energy through five trophic levels.  
    Losses due to **respiration** are shown as arrows to the **right**,  
    while losses due to **decomposition** are shown as arrows to the **left**.
    
    The example values are:
    
    - **Primary Producer (PP):** 1000 J received from the Sun  
      &rarr; 600 J lost to respiration, 200 J lost to decomposition, 200 J passed on.
    - **Primary Consumer (PC):** 200 J received from PP  
      &rarr; 120 J lost to respiration, 40 J lost to decomposition, 40 J passed on.
    - **Secondary Consumer (SC):** 40 J received from PC  
      &rarr; 24 J lost to respiration, 8 J lost to decomposition, 8 J passed on.
    - **Apex Predator (AP):** 8 J received from SC  
      &rarr; 4 J lost to respiration, 3 J lost to decomposition (leaving 1 J net).
    """
)

# Create a Graphviz Digraph with a top-to-bottom layout
diagram = graphviz.Digraph(format='png')
diagram.attr(rankdir='TB')

# Define the main nodes with energy values
diagram.node("Sun", "Sun\n(1000 J)")
diagram.node("PP", "Primary Producer\n(1000 J input)")
diagram.node("PC", "Primary Consumer\n(200 J input)")
diagram.node("SC", "Secondary Consumer\n(40 J input)")
diagram.node("AP", "Apex Predator\n(8 J input)")

# Draw the main vertical energy flow edges
diagram.edge("Sun", "PP", label="1000 J sunlight")
diagram.edge("PP", "PC", label="200 J")
diagram.edge("PC", "SC", label="40 J")
diagram.edge("SC", "AP", label="8 J")

# --- Primary Producer losses ---
# Create extra nodes for losses at the Primary Producer level
diagram.node("PP_R", "Respiration\n600 J")
diagram.node("PP_D", "Decomposition\n200 J")
# Draw edges from PP to its loss nodes:
#   Use tailport and headport to encourage right (east) for respiration and left (west) for decomposition
diagram.edge("PP", "PP_R", label="600 J", tailport="e", headport="w")
diagram.edge("PP", "PP_D", label="200 J", tailport="w", headport="e")

# --- Primary Consumer losses ---
diagram.node("PC_R", "Respiration\n120 J")
diagram.node("PC_D", "Decomposition\n40 J")
diagram.edge("PC", "PC_R", label="120 J", tailport="e", headport="w")
diagram.edge("PC", "PC_D", label="40 J", tailport="w", headport="e")

# --- Secondary Consumer losses ---
diagram.node("SC_R", "Respiration\n24 J")
diagram.node("SC_D", "Decomposition\n8 J")
diagram.edge("SC", "SC_R", label="24 J", tailport="e", headport="w")
diagram.edge("SC", "SC_D", label="8 J", tailport="w", headport="e")

# --- Apex Predator losses ---
diagram.node("AP_R", "Respiration\n4 J")
diagram.node("AP_D", "Decomposition\n3 J")
diagram.edge("AP", "AP_R", label="4 J", tailport="e", headport="w")
diagram.edge("AP", "AP_D", label="3 J", tailport="w", headport="e")

st.graphviz_chart(diagram)
