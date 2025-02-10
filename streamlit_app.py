import streamlit as st
import graphviz

st.title("Energy Transfer Diagram with Losses & Efficiency")
st.markdown(
    """
This diagram shows the energy flow through five trophic levels.  
For each level the **input energy** is divided into:
- **Decomposition** losses (placed on the **left**)
- **Respiration** losses (placed on the **right**)

The remaining energy is transferred to the next trophic level.  
Transfer efficiency is calculated as:  

\\[
\\text{Efficiency} = \\frac{\\text{Transferred Energy}}{\\text{Input Energy}} \\times 100\\%
\\]

**Example Values:**

- **Primary Producer:**  
  Input = 1000 J, Respiration = 600 J, Decomposition = 200 J  
  Transfer = 1000 - (600 + 200) = 200 J, Efficiency = 20%

- **Primary Consumer:**  
  Input = 200 J, Respiration = 120 J, Decomposition = 40 J  
  Transfer = 200 - (120 + 40) = 40 J, Efficiency = 20%

- **Secondary Consumer:**  
  Input = 40 J, Respiration = 24 J, Decomposition = 8 J  
  Transfer = 40 - (24 + 8) = 8 J, Efficiency = 20%

- **Apex Predator:**  
  Input = 8 J, Respiration = 4 J, Decomposition = 3 J  
  Transfer = 8 - (4 + 3) = 1 J, Efficiency ≈ 12.5%
    """
)

# Create a Graphviz Digraph with a top-to-bottom layout.
diagram = graphviz.Digraph(format='png')
diagram.attr(rankdir='TB')

# --- Sun Node ---
diagram.node("Sun", "Sun\n(1000 J)")

# --- Primary Producer Group ---
with diagram.subgraph(name='cluster_PP') as pp:
    pp.attr(rank='same')
    # Order nodes from left to right: Decomposition, Main, Respiration
    pp.node("PP_decomp", "Decomposition\n200 J")
    pp.node("PP_main", "Primary Producer\nInput: 1000 J")
    pp.node("PP_resp", "Respiration\n600 J")
    # Invisible edges to enforce horizontal order
    pp.edge("PP_decomp", "PP_main", style="invis")
    pp.edge("PP_main", "PP_resp", style="invis")

# --- Primary Consumer Group ---
with diagram.subgraph(name='cluster_PC') as pc:
    pc.attr(rank='same')
    pc.node("PC_decomp", "Decomposition\n40 J")
    pc.node("PC_main", "Primary Consumer\nInput: 200 J")
    pc.node("PC_resp", "Respiration\n120 J")
    pc.edge("PC_decomp", "PC_main", style="invis")
    pc.edge("PC_main", "PC_resp", style="invis")

# --- Secondary Consumer Group ---
with diagram.subgraph(name='cluster_SC') as sc:
    sc.attr(rank='same')
    sc.node("SC_decomp", "Decomposition\n8 J")
    sc.node("SC_main", "Secondary Consumer\nInput: 40 J")
    sc.node("SC_resp", "Respiration\n24 J")
    sc.edge("SC_decomp", "SC_main", style="invis")
    sc.edge("SC_main", "SC_resp", style="invis")

# --- Apex Predator Group ---
with diagram.subgraph(name='cluster_AP') as ap:
    ap.attr(rank='same')
    ap.node("AP_decomp", "Decomposition\n3 J")
    ap.node("AP_main", "Apex Predator\nInput: 8 J")
    ap.node("AP_resp", "Respiration\n4 J")
    ap.edge("AP_decomp", "AP_main", style="invis")
    ap.edge("AP_main", "AP_resp", style="invis")

# --- Connect the Trophic Levels ---
# Connect Sun to Primary Producer main node:
diagram.edge("Sun", "PP_main", label="1000 J from sunlight")

# Primary Producer to Primary Consumer:
# Transfer = 1000 - (600+200) = 200 J; Efficiency = 20%
diagram.edge("PP_main", "PC_main", label="Transfer: 200 J\nEfficiency: 20%")

# Primary Consumer to Secondary Consumer:
# Transfer = 200 - (120+40) = 40 J; Efficiency = 20%
diagram.edge("PC_main", "SC_main", label="Transfer: 40 J\nEfficiency: 20%")

# Secondary Consumer to Apex Predator:
# Transfer = 40 - (24+8) = 8 J; Efficiency = 20%
diagram.edge("SC_main", "AP_main", label="Transfer: 8 J\nEfficiency: 20%")

# Apex Predator net energy (optional display)
# Net Energy = 8 - (4+3) = 1 J; Efficiency ≈ 12.5%
diagram.node("AP_net", "Net Energy: 1 J\nEfficiency: 12.5%")
diagram.edge("AP_main", "AP_net", style="dotted", arrowhead="none")

st.graphviz_chart(diagram)
