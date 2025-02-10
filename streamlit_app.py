import streamlit as st
import graphviz

st.title("Energy Transfer with Losses and Efficiency Calculations")
st.markdown(
    r"""
This diagram illustrates the flow of energy through five trophic levels.  
For each level, the **input energy** is partitioned into losses due to **respiration** and **decomposition** (shown on the same horizontal line as the trophic node), with arrows indicating the direction of the loss:
- **Respiration** losses are shown to the **right**.
- **Decomposition** losses are shown to the **left**.

The remaining energy is transferred to the next trophic level, and the **transfer efficiency** is calculated as:

\[
\text{Efficiency} = \frac{\text{Transferred Energy}}{\text{Input Energy}} \times 100\%
\]

**Example Values:**

- **Primary Producer:**  
  Input: 1000 J  
  Respiration: 600 J, Decomposition: 200 J  
  Transferred: \(1000 - (600 + 200) = 200\) J, Efficiency: \( \frac{200}{1000} \times 100 = 20\% \)

- **Primary Consumer:**  
  Input: 200 J  
  Respiration: 120 J, Decomposition: 40 J  
  Transferred: \(200 - (120 + 40) = 40\) J, Efficiency: 20%

- **Secondary Consumer:**  
  Input: 40 J  
  Respiration: 24 J, Decomposition: 8 J  
  Transferred: \(40 - (24 + 8) = 8\) J, Efficiency: 20%

- **Apex Predator:**  
  Input: 8 J  
  Respiration: 4 J, Decomposition: 3 J  
  Transferred (Net): \(8 - (4 + 3) = 1\) J, Efficiency: \( \frac{1}{8} \times 100 \approx 12.5\% \)
    """
)

# Create a Graphviz Digraph with a top-to-bottom layout.
diagram = graphviz.Digraph(format='png')
diagram.attr(rankdir='TB')

# --- Sun Node ---
diagram.node("Sun", "Sun\n(1000 J)")

# --- Primary Producer Group ---
# We force the ordering within this subgraph so that the decomposition node appears on the left,
# the main (trophic) node in the center, and the respiration node on the right.
with diagram.subgraph(name="cluster_PP") as pp:
    pp.attr(rank='same')
    pp.node("PP_decomp", "Decomposition\n200 J")
    pp.node("PP_main", "Primary Producer\nInput: 1000 J")
    pp.node("PP_resp", "Respiration\n600 J")
    # Invisible edges enforce left-to-right ordering.
    pp.edge("PP_decomp", "PP_main", style="invis")
    pp.edge("PP_main", "PP_resp", style="invis")

# --- Primary Consumer Group ---
with diagram.subgraph(name="cluster_PC") as pc:
    pc.attr(rank='same')
    pc.node("PC_decomp", "Decomposition\n40 J")
    pc.node("PC_main", "Primary Consumer\nInput: 200 J")
    pc.node("PC_resp", "Respiration\n120 J")
    pc.edge("PC_decomp", "PC_main", style="invis")
    pc.edge("PC_main", "PC_resp", style="invis")

# --- Secondary Consumer Group ---
with diagram.subgraph(name="cluster_SC") as sc:
    sc.attr(rank='same')
    sc.node("SC_decomp", "Decomposition\n8 J")
    sc.node("SC_main", "Secondary Consumer\nInput: 40 J")
    sc.node("SC_resp", "Respiration\n24 J")
    sc.edge("SC_decomp", "SC_main", style="invis")
    sc.edge("SC_main", "SC_resp", style="invis")

# --- Apex Predator Group ---
with diagram.subgraph(name="cluster_AP") as ap:
    ap.attr(rank='same')
    ap.node("AP_decomp", "Decomposition\n3 J")
    ap.node("AP_main", "Apex Predator\nInput: 8 J")
    ap.node("AP_resp", "Respiration\n4 J")
    ap.edge("AP_decomp", "AP_main", style="invis")
    ap.edge("AP_main", "AP_resp", style="invis")

# --- Vertical Energy Flow Between Trophic Levels ---
# Connect the Sun to the Primary Producer:
diagram.edge("Sun", "PP_main", label="1000 J from sunlight")

# For Primary Producer:
# Transferred Energy = 1000 - (600 + 200) = 200 J; Efficiency = 20%
diagram.edge("PP_main", "PC_main", label="Transfer: 200 J\nEfficiency: 20%")

# For Primary Consumer:
# Transferred Energy = 200 - (120 + 40) = 40 J; Efficiency = 20%
diagram.edge("PC_main", "SC_main", label="Transfer: 40 J\nEfficiency: 20%")

# For Secondary Consumer:
# Transferred Energy = 40 - (24 + 8) = 8 J; Efficiency = 20%
diagram.edge("SC_main", "AP_main", label="Transfer: 8 J\nEfficiency: 20%")

# For Apex Predator, show its net energy (no further transfer):
diagram.node("AP_net", "Net Energy: 1 J\nEfficiency: 12.5%")
diagram.edge("AP_main", "AP_net", style="dotted", arrowhead="none")

# --- Arrows for Respiration and Decomposition Losses ---
# For Primary Producer:
diagram.edge("PP_main", "PP_resp", label="600 J", tailport="e", headport="w")
diagram.edge("PP_main", "PP_decomp", label="200 J", tailport="w", headport="e")

# For Primary Consumer:
diagram.edge("PC_main", "PC_resp", label="120 J", tailport="e", headport="w")
diagram.edge("PC_main", "PC_decomp", label="40 J", tailport="w", headport="e")

# For Secondary Consumer:
diagram.edge("SC_main", "SC_resp", label="24 J", tailport="e", headport="w")
diagram.edge("SC_main", "SC_decomp", label="8 J", tailport="w", headport="e")

# For Apex Predator:
diagram.edge("AP_main", "AP_resp", label="4 J", tailport="e", headport="w")
diagram.edge("AP_main", "AP_decomp", label="3 J", tailport="w", headport="e")

st.graphviz_chart(diagram)
