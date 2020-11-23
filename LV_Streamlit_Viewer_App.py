import streamlit as st
import pandas as pd
import altair as alt

import requests


st.header("Du Chemin Lost Voices Cadence Data")

# st.cache speeds things up by holding data in cache
# @st.cache
@st.cache(allow_output_mutation=True)
def get_data():
    url = "https://raw.githubusercontent.com/RichardFreedman/LostVoicesCadenceViewer/main/LV_CadenceData.csv"
    df = pd.read_csv(url)
    cadence_json =  requests.get("https://raw.githubusercontent.com/bmill42/DuChemin/master/phase1/data/duchemin.similarities.json").json()
    df['similarity'] = cadence_json
    return df 
df = get_data()



# Dialogue to Show Raw Data as Table

if st.sidebar.checkbox('Show Complete Data Frame'):
	st.subheader('Raw data')
	st.write(df)

#tones = df['cadence_final_tone'].drop_duplicates()
#tones = df[["cadence_final_tone", "cadence_kind", "final_cadence", "composition_number"]]

if st.sidebar.checkbox('Show Cadence Counts'):
    st.subheader('Cadence Counts')
    st.write(df['cadence_final_tone'].value_counts())

#tones = df['cadence_final_tone'].drop_duplicates()
tones = df[["cadence_final_tone", "cadence_kind", "final_cadence", "composition_number"]]

all_tone_1 = alt.Chart(tones).mark_circle().encode(
    x='cadence_final_tone',
    y='final_cadence',
    color='cadence_kind'
)

if st.sidebar.checkbox('Cadence Kinds and Tones'):
    st.subheader('Cadence Kinds and Tones')
    st.altair_chart(all_tone_1, use_container_width=True)


# This displays unfiltered 

all_tone_diagram = alt.Chart(tones).mark_circle().encode(
    x='final_cadence',
    y='composition_number',
    color='cadence_final_tone',
    shape='cadence_kind'
)

if st.sidebar.checkbox('Show All Pieces with Their Cadences'):
	st.subheader('All Pieces with Cadences')
	st.altair_chart(all_tone_diagram, use_container_width=True)


# Dialogue to Select Cadence by Final Tone
st.subheader('Cadences with Final Tone as Shown at Left')


# Create a list of possible values and multiselect menu with them in it.

#cadence_list = tones['cadence_final_tone']
cadence_list = tones['cadence_final_tone'].unique()
cadences_selected = st.sidebar.multiselect('Select Tone(s)', cadence_list)

# Mask to filter dataframe
mask_cadences = tones['cadence_final_tone'].isin(cadences_selected)

tone_data = tones[mask_cadences]

# This is for filtered tones (just oned)
tone_diagram = alt.Chart(tone_data).mark_circle().encode(
    x='cadence_kind',
    y='composition_number',
    color='final_cadence',
    #shape='final_cadence',
    tooltip=['cadence_kind', 'composition_number', 'final_cadence']
)

st.altair_chart(tone_diagram, use_container_width=True)


# This displays choice of piece 
st.subheader('Selected Pieces as Shown at Left')

piece_list = tones['composition_number'].unique()
pieces_selected = st.sidebar.multiselect('Select Piece(s)', piece_list)

# Mask to filter dataframe
mask_pieces = tones['composition_number'].isin(pieces_selected)

piece_data = tones[mask_pieces]
piece_diagram = alt.Chart(piece_data).mark_circle().encode(
    x='cadence_final_tone',
    y='cadence_kind',
    color='final_cadence',
    #shape='final_cadence'
)

st.altair_chart(piece_diagram, use_container_width=True)



#similar_cadences = df[["phrase_number", "similarity"]]

#st.plotly_chart(similar_cadences)







