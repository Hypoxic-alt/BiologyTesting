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
    pp_eff = round(random.uniform(7, 15), 1)
    pp_input = sun
    pp_transfer = pp_input * (pp_eff / 100)
    pp_losses = pp_input - pp_transfer
    pp_resp = int(round(0.75 * pp_losses))
    pp_decomp = int(round(pp_losses - pp_resp))
    data['PP'] = {
        "input": int(round(pp_input)),
        "eff": pp_eff,
        "transfer": int(round(pp_transfer)),
        "losses": int(round(pp_losses)),
        "resp": pp_resp,
        "decomp": pp_decomp
    }

    # Primary Consumer (PC)
    pc_input = pp_transfer
    pc_eff = round(random.uniform(7, 15), 1)
    pc_transfer = pc_input * (pc_eff / 100)
    pc_losses = pc_input - pc_transfer
    pc_resp = int(round(0.75 * pc_losses))
    pc_decomp = int(round(pc_losses - pc_resp))
    data['PC'] = {
        "input": int(round(pc_input)),
        "eff": pc_eff,
        "transfer": int(round(pc_transfer)),
        "losses": int(round(pc_losses)),
        "resp": pc_resp,
        "decomp": pc_decomp
    }

    # Secondary Consumer (SC)
    sc_input = pc_transfer
    sc_eff = round(random.uniform(7, 15), 1)
    sc_transfer = sc_input * (sc_eff / 100)
    sc_losses = sc_input - sc_transfer
    sc_resp = int(round(0.75 * sc_losses))
    sc_decomp = int(round(sc_losses - sc_resp))
    data['SC'] = {
        "input": int(round(sc_input)),
        "eff": sc_eff,
        "transfer": int(round(sc_transfer)),
        "losses": int(round(sc_losses)),
        "resp": sc_resp,
        "decomp": sc_decomp
    }

    # Apex Predator (AP)
    ap_input = sc_transfer
    ap_eff = round(random.uniform(7, 15), 1)
    ap_net = ap_input * (ap_eff / 100)
    ap_losses = ap_input - ap_net
    ap_resp = int(round(0.75 * ap_losses))
    ap_decomp = int(round(ap_losses - ap_resp))
    data['AP'] = {
        "input": int(round(ap_input)),
        "eff": ap_eff,
        "net": int(round(ap_net)),
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

# Button to show answers (i.e. display efficiencies)
if st.button("Show Answer"):
    st.session_state['show_answers'] = True

data = st.session_state['data']
show_ans = st.session_state['show_answers']

# Create a Graphviz Digraph (vertical top-to-bottom)
diagram = graphviz.Digraph(format='png')
diagram.attr(rankdir='TB')

# Sun node
diagram.node("Sun", f"Sun\n({data['sun']} J)")

# Create nodes for each trophic level using HTML tables.
# Primary Producer (PP)
pp_label = f'''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>Decomposition<br/>{data['PP']['decomp']} J</TD>
    <TD>Primary Producer<br/>Input: {data['PP']['input']} J</TD>
    <TD>Respiration<br/>{data['PP']['resp']} J</TD>
  </TR>
</TABLE>
>'''
diagram.node("PP", pp_label)

# Primary Consumer (PC)
pc_label = f'''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>Decomposition<br/>{data['PC']['decomp']} J</TD>
    <TD>Primary Consumer<br/>Input: {data['PC']['input']} J</TD>
    <TD>Respiration<br/>{data['PC']['resp']} J</TD>
  </TR>
</TABLE>
>'''
diagram.node("PC", pc_label)

# Secondary Consumer (SC)
sc_label = f'''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>Decomposition<br/>{data['SC']['decomp']} J</TD>
    <TD>Secondary Consumer<br/>Input: {data['SC']['input']} J</TD>
    <TD>Respiration<br/>{data['SC']['resp']} J</TD>
  </TR>
</TABLE>
>'''
diagram.node("SC", sc_label)

# Apex Predator (AP)
ap_label = f'''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>Decomposition<br/>{data['AP']['decomp']} J</TD>
    <TD>Apex Predator<br/>Input: {data['AP']['input']} J</TD>
    <TD>Respiration<br/>{data['AP']['resp']} J</TD>
  </TR>
</TABLE>
>'''
diagram.node("AP", ap_label)

# Vertical connections (edges)
# Sun to Primary Producer
diagram.edge("Sun", "PP", label=f"{data['sun']} J from sunlight")

# Primary Producer to Primary Consumer
pp_edge_label = f"Transfer: {data['PP']['transfer']} J"
if show_ans:
    pp_edge_label += f"\nEfficiency: {data['PP']['eff']}%"
diagram.edge("PP", "PC", label=pp_edge_label)

# Primary Consumer to Secondary Consumer
pc_edge_label = f"Transfer: {data['PC']['transfer']} J"
if show_ans:
    pc_edge_label += f"\nEfficiency: {data['PC']['eff']}%"
diagram.edge("PC", "SC", label=pc_edge_label)

# Secondary Consumer to Apex Predator
sc_edge_label = f"Transfer: {data['SC']['transfer']} J"
if show_ans:
    sc_edge_label += f"\nEfficiency: {data['SC']['eff']}%"
diagram.edge("SC", "AP", label=sc_edge_label)

# For Apex Predator, show net energy in an extra node.
diagram.node("AP_net", f"Net Energy: {data['AP']['net']} J" + (f"\nEfficiency: {data['AP']['eff']}%" if show_ans else ""))
diagram.edge("AP", "AP_net", style="dotted", arrowhead="none")

st.graphviz_chart(diagram)
