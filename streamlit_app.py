import streamlit as st
import graphviz
import random

def generate_data():
    """Generate random energy values and efficiencies for each trophic level."""
    data = {}
    # Random Sun energy between 30,000 and 80,000 J
    sun = random.randint(30000, 80000)
    data['sun'] = sun

    # Primary Producer (PP)
    # For primary producers, we interpret the input energy as GPP.
    pp_eff = round(random.uniform(7, 15), 1)
    pp_GPP = sun  # Assume the plant captures all the sun energy available in this simplified model.
    pp_NPP = pp_GPP * (pp_eff / 100)  # NPP is the net energy available for transfer.
    pp_losses = pp_GPP - pp_NPP
    pp_resp = int(round(0.75 * pp_losses))
    pp_decomp = int(round(pp_losses - pp_resp))
    data['PP'] = {
        "GPP": int(round(pp_GPP)),
        "NPP": int(round(pp_NPP)),
        "eff": pp_eff,
        "losses": int(round(pp_losses)),
        "resp": pp_resp,
        "decomp": pp_decomp
    }

    # Primary Consumer (PC)
    # For heterotrophs we continue to use "input" as the energy they receive.
    pc_input = pp_NPP
    pc_eff = round(random.uniform(7, 15), 1)
    pc_transfer = pc_input * (pc_eff / 100)
    pc_losses = pc_input - pc_transfer
    pc_resp = int(round(0.75 * pc_losses))
    pc_decomp = int(round(pc_losses - pc_resp))
    data['PC'] = {
        "input": int(round(pc_input)),
        "transfer": int(round(pc_transfer)),
        "eff": pc_eff,
        "losses": int(round(pc_losses)),
        "resp": pc_resp,
        "decomp": pc_decomp
    }

    # Secondary Consumer (SC)
    sc_input = data['PC']["transfer"]
    sc_eff = round(random.uniform(7, 15), 1)
    sc_transfer = sc_input * (sc_eff / 100)
    sc_losses = sc_input - sc_transfer
    sc_resp = int(round(0.75 * sc_losses))
    sc_decomp = int(round(sc_losses - sc_resp))
    data['SC'] = {
        "input": int(round(sc_input)),
        "transfer": int(round(sc_transfer)),
        "eff": sc_eff,
        "losses": int(round(sc_losses)),
        "resp": sc_resp,
        "decomp": sc_decomp
    }

    # Apex Predator (AP)
    ap_input = data['SC']["transfer"]
    ap_eff = round(random.uniform(7, 15), 1)
    ap_net = ap_input * (ap_eff / 100)
    ap_losses = ap_input - ap_net
    ap_resp = int(round(0.75 * ap_losses))
    ap_decomp = int(round(ap_losses - ap_resp))
    data['AP'] = {
        "input": int(round(ap_input)),
        "net": int(round(ap_net)),
        "eff": ap_eff,
        "losses": int(round(ap_losses)),
        "resp": ap_resp,
        "decomp": ap_decomp
    }
    return data

# Initialize session state for the data and whether answers are shown.
if 'data' not in st.session_state:
    st.session_state['data'] = generate_data()
if 'show_answers' not in st.session_state:
    st.session_state['show_answers'] = False

# Button to randomize values
if st.button("Randomize Values"):
    st.session_state['data'] = generate_data()
    st.session_state['show_answers'] = False

# Button to show answers (i.e. display efficiencies and their calculations)
if st.button("Show Answer"):
    st.session_state['show_answers'] = True

data = st.session_state['data']
show_ans = st.session_state['show_answers']

# Create a Graphviz Digraph with a top-to-bottom layout.
diagram = graphviz.Digraph(format='png')
diagram.attr(rankdir='TB')

# Sun node
diagram.node("Sun", f"Sun\n({data['sun']} J)")

# Use an HTML table for each trophic level node.
def build_level_node(display_name, level_data, is_primary=False):
    if is_primary:
        # For the primary producer, show GPP and NPP.
        center_text = f"GPP: {level_data['GPP']} J<br/>NPP: {level_data['NPP']} J"
    else:
        center_text = f"Input: {level_data['input']} J"
    return f'''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>Decomposition<br/>{level_data['decomp']} J</TD>
    <TD>{display_name}<br/>{center_text}</TD>
    <TD>Respiration<br/>{level_data['resp']} J</TD>
  </TR>
</TABLE>
>'''

# Primary Producer node (labeled with GPP/NPP)
diagram.node("PP", build_level_node("Primary Producer", data['PP'], is_primary=True))

# Primary Consumer node
diagram.node("PC", build_level_node("Primary Consumer", data['PC']))

# Secondary Consumer node
diagram.node("SC", build_level_node("Secondary Consumer", data['SC']))

# Apex Predator node
diagram.node("AP", build_level_node("Apex Predator", data['AP']))

# Vertical connections (edges)
# Sun to Primary Producer: here the sunlight leads to the PP's GPP.
diagram.edge("Sun", "PP", label=f"Sunlight: {data['sun']} J")

# Primary Producer to Primary Consumer: now label the transferred energy as NPP.
pp_edge_label = f"NPP: {data['PP']['NPP']} J"
if show_ans:
    pp_edge_label += f"\nEfficiency: {data['PP']['eff']}% ( {data['PP']['NPP']} J / {data['PP']['GPP']} J * 100 )"
diagram.edge("PP", "PC", label=pp_edge_label)

# Primary Consumer to Secondary Consumer
pc_edge_label = f"Transfer: {data['PC']['transfer']} J"
if show_ans:
    pc_edge_label += f"\nEfficiency: {data['PC']['eff']}% ( {data['PC']['transfer']} J / {data['PC']['input']} J * 100 )"
diagram.edge("PC", "SC", label=pc_edge_label)

# Secondary Consumer to Apex Predator
sc_edge_label = f"Transfer: {data['SC']['transfer']} J"
if show_ans:
    sc_edge_label += f"\nEfficiency: {data['SC']['eff']}% ( {data['SC']['transfer']} J / {data['SC']['input']} J * 100 )"
diagram.edge("SC", "AP", label=sc_edge_label)

# For Apex Predator, show net energy in an extra node.
ap_net_label = f"Net Energy: {data['AP']['net']} J"
if show_ans:
    ap_net_label += f"\nEfficiency: {data['AP']['eff']}% ( {data['AP']['net']} J / {data['AP']['input']} J * 100 )"
diagram.node("AP_net", ap_net_label)
diagram.edge("AP", "AP_net", style="dotted", arrowhead="none")

st.graphviz_chart(diagram)
