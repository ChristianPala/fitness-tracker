import streamlit as st
import pandas as pd
from datetime import date

# Routine dictionary
routine = {
    'Lunedì': ["Panca Piana", "Military Press", "Lat Machine", "Squat"],
    'Mercoledì': ["Affondi", "Stacchi Rumeni", "Spinte con Manubri su Panca Inclinata", "Rematore"],
    'Venerdì': ["Lat Machine", "Rematore", "Military Press", "Squat"]
}

if 'workouts' not in st.session_state:
    st.session_state.workouts = []
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

st.title("Traccia i tuoi allenamenti")

# Add new or edit mode
if st.session_state.edit_index is None:
    st.header("Aggiungi nuova sessione")
    day = st.selectbox("Giorno della settimana", list(routine.keys()))
    exercise = st.selectbox("Esercizio", routine[day])
    session_date = st.date_input("Data", value=date.today())
    weight = st.number_input("Peso (kg)", min_value=0.0, step=0.5)
    notes = st.text_input("Note (opzionale)")
else:
    st.header("Modifica sessione")
    row = st.session_state.workouts[st.session_state.edit_index]
    day = st.selectbox("Giorno della settimana", list(routine.keys()), index=list(routine.keys()).index(row["Giorno"]))
    exercise = st.selectbox("Esercizio", routine[day], index=routine[day].index(row["Esercizio"]))
    session_date = st.date_input("Data", value=row["Data"])
    weight = st.number_input("Peso (kg)", min_value=0.0, step=0.5, value=row["Peso"])
    notes = st.text_input("Note (opzionale)", value=row["Note"])

# Save or update
if st.session_state.edit_index is None:
    if st.button("Salva sessione"):
        st.session_state.workouts.append({
            "Data": session_date,
            "Giorno": day,
            "Esercizio": exercise,
            "Peso": weight,
            "Note": notes
        })
        st.success("Sessione salvata!")
else:
    if st.button("Aggiorna sessione"):
        st.session_state.workouts[st.session_state.edit_index] = {
            "Data": session_date,
            "Giorno": day,
            "Esercizio": exercise,
            "Peso": weight,
            "Note": notes
        }
        st.session_state.edit_index = None
        st.success("Sessione aggiornata!")
    if st.button("Annulla"):
        st.session_state.edit_index = None

# Group and show sessions
st.subheader("Storico allenamenti")

df = pd.DataFrame(st.session_state.workouts)
if not df.empty:
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_exercise = st.selectbox("Filtra per esercizio", ["Tutti"] + sorted(df["Esercizio"].unique()))
    with col2:
        filter_day = st.selectbox("Filtra per giorno", ["Tutti"] + list(routine.keys()))

    filtered_df = df.copy()
    if filter_exercise != "Tutti":
        filtered_df = filtered_df[filtered_df["Esercizio"] == filter_exercise]
    if filter_day != "Tutti":
        filtered_df = filtered_df[filtered_df["Giorno"] == filter_day]
    filtered_df = filtered_df.reset_index(drop=True)

    # Show table with edit/delete
    for i, row in filtered_df.iterrows():
        st.write(f"**{row['Data']}** | {row['Giorno']} | {row['Esercizio']} | {row['Peso']} kg | {row['Note']}")
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("Modifica", key=f"edit_{i}"):
                # Find real index in full list
                idx = df.index[(df['Data'] == row['Data']) & (df['Giorno'] == row['Giorno']) & 
                               (df['Esercizio'] == row['Esercizio']) & (df['Peso'] == row['Peso']) & 
                               (df['Note'] == row['Note'])][0]
                st.session_state.edit_index = idx
                st.rerun()
        with col2:
            if st.button("Elimina", key=f"delete_{i}"):
                idx = df.index[(df['Data'] == row['Data']) & (df['Giorno'] == row['Giorno']) & 
                               (df['Esercizio'] == row['Esercizio']) & (df['Peso'] == row['Peso']) & 
                               (df['Note'] == row['Note'])][0]
                st.session_state.workouts.pop(idx)
                st.rerun()
else:
    st.info("Nessuna sessione ancora.")

