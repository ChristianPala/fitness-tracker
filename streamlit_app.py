import streamlit as st
import pandas as pd
from datetime import date

# List of exercises per day
routine = {
    'Lunedì': ["Panca Piana", "Military Press", "Lat Machine", "Squat"],
    'Mercoledì': ["Affondi", "Stacchi Rumeni", "Spinte con Manubri su Panca Inclinata", "Rematore"],
    'Venerdì': ["Lat Machine", "Rematore", "Military Press", "Squat"]
}

# App state: store data
if 'workouts' not in st.session_state:
    st.session_state.workouts = []

st.title("Traccia i tuoi allenamenti")

# Select day
day = st.selectbox("Giorno della settimana", list(routine.keys()))

# Select exercise
exercise = st.selectbox("Esercizio", routine[day])

# Input fields
col1, col2 = st.columns(2)
with col1:
    session_date = st.date_input("Data", value=date.today())
with col2:
    weight = st.number_input("Peso utilizzato (kg)", min_value=0.0, step=0.5)

notes = st.text_input("Note (opzionale)")

if st.button("Salva sessione"):
    st.session_state.workouts.append({
        "Data": session_date,
        "Giorno": day,
        "Esercizio": exercise,
        "Peso": weight,
        "Note": notes
    })
    st.success("Sessione salvata!")

# Show all saved sessions
df = pd.DataFrame(st.session_state.workouts)
if not df.empty:
    st.subheader("Storico allenamenti")
    st.dataframe(df)
else:
    st.info("Nessun allenamento registrato ancora.")
