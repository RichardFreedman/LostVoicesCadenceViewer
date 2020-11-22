import streamlit as st
import pandas as pd
import altair as alt

st.header("Du Chemin Lost Voices Cadence Data")

@st.cache
def get_data():
	path = r'/Users/rfreedma/Downloads/Du Chemin Production Data - Similar_Cadences.csv'
	return pd.read_csv(path)
df = get_data()

# Dialogue to Show Raw Data as Table

if st.sidebar.checkbox('Show Complete Data Frame'):
	st.subheader('Raw data')
	st.write(df)

#tones = df['cadence_final_tone'].drop_duplicates()
tones = df[["cadence_final_tone", "cadence_kind", "final_cadence", "composition_number"]]


# This displays unfiltered 

all_tone_diagram = alt.Chart(tones).mark_circle().encode(
    x='cadence_kind',
    y='composition_number',
    color='final_cadence',
    #shape='final_cadence'
)

if st.sidebar.checkbox('Show All Pieces with Their Cadences'):
	st.subheader('All Pieces with Cadences')
	st.altair_chart(all_tone_diagram, use_container_width=True)


# Dialogue to Select Cadence by Final Tone
st.subheader('Selected Cadences by Final Tone')


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
st.subheader('Selected Pieces')

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







