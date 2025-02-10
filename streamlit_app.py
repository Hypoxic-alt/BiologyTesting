import streamlit as st
import graphviz

st.title("Energy Transfer with Losses and Efficiency Calculations")
st.markdown(
    """
This diagram illustrates the flow of energy through five trophic levels.  
For each level, the **input energy** is split into energy lost to **respiration** and **decomposition** (both shown on the same horizontal level as the trophic node), with the remaining energy transferred to the next trophic level.

The trophic transfer efficiency is calculated as:  
\\( \\text{Efficiency} = \\frac{\\text{Transferred Energy}}{\\text{Input Energy}} \\times 100\\% \\)

**Example Values:**

- **Primary Producer:** Input: 1000 J, Respiration: 600 J, Decomposition: 200 J, Transfer: 200 J, Efficiency: 20%
- **Primary Consumer:** Input: 200 J, Respiration: 120 J, Decomposition: 40 J, Transfer: 40 J, Efficiency: 20%
- **Secondary Consumer:** Input: 40 J, Respiration: 24 J, Decomposition: 8 J, Transfer: 8 J, Efficiency: 20%
- **Apex Predator:** Input: 8 J, Respiration: 4 J, Decomposition: 3 J, Transfer: 1 J, Efficiency: 12.5%
    """
)

# Create a Graphviz Digraph with a top-to-bottom layout.
diagram = graphviz.Digraph(format='png')
diagram.attr(rankdir='TB')

# --- Sun Node ---
diagram.node("Sun", "Sun\n(1000 J)")

# --- Primary Producer Group ---
# Group the Primary Producer’s main energy and its losses on the same horizontal level.
with diagram.subgraph() as pp:
    pp.attr(rank='same')
    pp.node("PP_main", "Primary Producer\nInput: 1000 J")
    pp.node("PP_resp", "Respiration\n600 J")
    pp.node("PP_decomp", "Decomposition\n200 J")

# --- Primary Consumer Group ---
with diagram.subgraph() as pc:
    pc.attr(rank='same')
    pc.node("PC_main", "Primary Consumer\nInput: 200 J")
    pc.node("PC_resp", "Respiration\n120 J")
    pc.node("PC_decomp", "Decomposition\n40 J")

# --- Secondary Consumer Group ---
with diagram.subgraph() as sc:
    sc.attr(rank='same')
    sc.node("SC_main", "Secondary Consumer\nInput: 40 J")
    sc.node("SC_resp", "Respiration\n24 J")
    sc.node("SC_decomp", "Decomposition\n8 J")

# --- Apex Predator Group ---
with diagram.subgraph() as ap:
    ap.attr(rank='same')
    ap.node("AP_main", "Apex Predator\nInput: 8 J")
    ap.node("AP_resp", "Respiration\n4 J")
    ap.node("AP_decomp", "Decomposition\n3 J")

# --- Connect the Trophic Levels ---
# From Sun to Primary Producer:
diagram.edge("Sun", "PP_main", label="1000 J from sunlight")

# For Primary Producer:
# Transfer = 1000 - (600 + 200) = 200 J; Efficiency = (200/1000)*100 = 20%
diagram.edge("PP_main", "PC_main", label="Transfer: 200 J\nEfficiency: 20%")

# For Primary Consumer:
# Transfer = 200 - (120 + 40) = 40 J; Efficiency = 20%
diagram.edge("PC_main", "SC_main", label="Transfer: 40 J\nEfficiency: 20%")

# For Secondary Consumer:
# Transfer = 40 - (24 + 8) = 8 J; Efficiency = 20%
diagram.edge("SC_main", "AP_main", label="Transfer: 8 J\nEfficiency: 20%")

# For Apex Predator, while there is no further trophic transfer,
# we can optionally show its net energy and efficiency:
# Net Energy = 8 - (4 + 3) = 1 J; Efficiency = (1/8)*100 ≈ 12.5%
diagram.node("AP_net", "Net Energy: 1 J\nEfficiency: 12.5%")
diagram.edge("AP_main", "AP_net", style="dotted", arrowhead="none")

st.graphviz_chart(diagram)
