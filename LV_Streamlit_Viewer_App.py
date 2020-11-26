import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path
import requests

# sets up function to call Markdown File for "about"
def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

#main heading of the resource

st.header("Du Chemin Lost Voices Cadence Data")

#checkbox to display details of markdown introduction

about_check = st.checkbox("About this Resource")
about_markdown = read_markdown_file("introduction.md")

if about_check:
    st.subheader('About')
    st.markdown(about_markdown, unsafe_allow_html=True)

# st.cache speeds things up by holding data in cache

@st.cache(allow_output_mutation=True)

# get the data function 
def get_data():
    url = "https://raw.githubusercontent.com/RichardFreedman/LostVoicesCadenceViewer/main/LV_CadenceData.csv"
    df = pd.read_csv(url)
    # The following adds the list of 'similar' cadences to the DF
    cadence_json =  requests.get("https://raw.githubusercontent.com/bmill42/DuChemin/master/phase1/data/duchemin.similarities.json").json()
    df['similarity'] = cadence_json
    return df 
df = get_data()

# Summary stacked bar chart listed by cadence tone

st.subheader('Summary of Cadence Tones by Kind')
chartA = alt.Chart(df).mark_bar().encode(
    alt.X("cadence_final_tone"),
    y='count()',
    color='cadence_kind'
).properties(
    title='Summary of Cadence Tones by Kind'
)
st.altair_chart(chartA, use_container_width=True)

# Summary stacked bar chart listed by cadence kind
st.subheader('Summary of Cadence Kind by Tone')
chartB = alt.Chart(df).mark_bar().encode(
    alt.X("cadence_kind"),
    y='count()',
    color='cadence_final_tone'
).properties(
    title='Summary of Cadence Kind by Tone'
)
st.altair_chart(chartB, use_container_width=True)

#old code for checkboxes to show various simple dataframe summaries:

#if st.sidebar.checkbox('Show Cadence Kind Counts'):
    #st.subheader('Cadence Kind Counts')
    #st.write(df['cadence_kind'].value_counts())   

# here just pulling a selection of the complete dataframe--some columns

cadence_data = df[["cadence_final_tone", "cadence_kind", "final_cadence", "composition_number", "phrase_number"]]

st.subheader('Select Views and Subsets at Left:  Results Below')
st.subheader('  ')

# Dialogue to Select Cadence by Final Tone of Cadence

# Create a list of possible values and multiselect menu with them in it.

cadence_list_1 = cadence_data['cadence_final_tone'].unique()
cadences_selected_1 = st.sidebar.multiselect('1. Select Cadence Final Tone(s)', cadence_list_1)

# Mask to filter dataframe:  returns only those "selected" in previous step
mask_cadences_1 = cadence_data['cadence_final_tone'].isin(cadences_selected_1)

# And now a new dataframe with only the elements that statisfy the conditions

cadence_data_masked_1 = cadence_data[mask_cadences_1]

#This is for filtered tones (just oned)
diagram_1 = alt.Chart(cadence_data_masked_1).mark_circle().encode(
    x='cadence_kind',
    y='composition_number',
    color='final_cadence',
    #shape='final_cadence',
    tooltip=['phrase_number', 'cadence_kind', 'final_cadence']
).properties(
    title='1. Cadence Final Tones'
)

st.altair_chart(diagram_1, use_container_width=True)

# Dialogue to Select Cadence Kind

# Create a list of possible values and multiselect menu with them in it.

cadence_list_2 = cadence_data['cadence_kind'].unique()
cadences_selected_2 = st.sidebar.multiselect('2. Select Cadence Kind(s)', cadence_list_2)

# Mask to filter dataframe
mask_cadences_2 = cadence_data['cadence_kind'].isin(cadences_selected_2)

cadence_data_masked_2= cadence_data[mask_cadences_2]

# This is for filtered tones (just oned)
diagram_2 = alt.Chart(cadence_data_masked_2).mark_circle().encode(
    x='cadence_final_tone',
    y='composition_number',
    color='final_cadence',
    #shape='final_cadence',
    tooltip=['phrase_number', 'cadence_final_tone', 'final_cadence']
).properties(
    title='2. Cadence Kinds'
)

st.altair_chart(diagram_2, use_container_width=True)
# Dialogue to Select Last Cadence of Piece
#

# Create a list of possible values and multiselect menu with them in it.

cadence_list_3 = cadence_data['final_cadence'].unique()
cadences_selected_3 = st.sidebar.multiselect('3. Select Tone of Last Cadence', cadence_list_3)

# Mask to filter dataframe
mask_cadences_3 = cadence_data['final_cadence'].isin(cadences_selected_3)

cadence_data_masked_3 = cadence_data[mask_cadences_3]

# This is for filtered tones (just oned)
diagram_3 = alt.Chart(cadence_data_masked_3).mark_circle().encode(
    x='cadence_final_tone',
    y='composition_number',
    color='cadence_kind',
    #shape='final_cadence',
    tooltip=['phrase_number', 'cadence_final_tone', 'final_cadence']
).properties(
    title='3. Final Cadence of Piece'
)

st.altair_chart(diagram_3, use_container_width=True)
# This displays choice of piece 
#st.subheader('Cadences of Pieces Selected at Left')

piece_list = cadence_data['composition_number'].unique()
pieces_selected = st.sidebar.multiselect('4. Select Piece(s)', piece_list)

# Mask to filter dataframe
mask_pieces = cadence_data['composition_number'].isin(pieces_selected)

piece_data = cadence_data[mask_pieces]
piece_diagram = alt.Chart(piece_data).mark_circle().encode(
    x='cadence_final_tone',
    y='cadence_kind',
    color='final_cadence',
    #shape='final_cadence'
    tooltip=['phrase_number', 'cadence_final_tone', 'cadence_kind']
).properties(
    title='4. Selected Pieces'
)

st.altair_chart(piece_diagram, use_container_width=True)

#Now the generic views and full data sets

all_tone_1 = alt.Chart(cadence_data).mark_circle().encode(
    x='cadence_final_tone',
    y='final_cadence',
    color='cadence_kind'
)
if st.sidebar.checkbox('Cadence Kinds and Tones Cross Table'):
    st.subheader('Cadence Kinds and Tones Cross Table')
    st.altair_chart(all_tone_1, use_container_width=True)




# table of pieces with details via hover

tone_diagram = alt.Chart(cadence_data).mark_circle().encode(
    x='cadence_kind',
    y='composition_number',
    color='final_cadence',
    #shape='final_cadence',
    tooltip=['phrase_number', 'cadence_final_tone', 'cadence_kind']
)

if st.sidebar.checkbox('All Pieces and Cadences (with details)'):
    st.subheader('All Pieces and Cadences: Hover for Details')
    st.altair_chart(tone_diagram, use_container_width=True)

#st.altair_chart(tone_diagram, use_container_width=True)

# to show full datafram
if st.sidebar.checkbox('Show Complete Data Frame'):
	st.subheader('Complete Data Frame')
	st.write(df)









