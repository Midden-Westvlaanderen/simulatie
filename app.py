# energie_simulatie_dagdelen.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Energieverbruik Simulatie", layout="wide")
st.title("🏡 Simulatie energieverbruik op basis van dagdeel-thermostaatgedrag")

st.markdown("Stel de temperatuur in per dagdeel en zie hoeveel energie je verbruikt.")

# 📋 Gebruikersinvoer
col1, col2, col3 = st.columns(3)

with col1:
    woningtype = st.selectbox("Woningtype", ["Appartement", "Rijwoning", "Halfopen woning", "Vrijstaande woning"])
with col2:
    isolatie = st.selectbox("Isolatieniveau", ["Slecht", "Matig", "Goed"])
with col3:
    oppervlakte = st.slider("Oppervlakte woning (m²)", 50, 300, 100)

gedrag = st.radio("Gedragstype", ["Zuinig", "Gemiddeld", "Royaal"], horizontal=True)

# 🌡️ Temperatuur per dagdeel
st.subheader("🌤️ Thermostaatinstellingen per dagdeel")

col_a, col_b, col_c, col_d, col_e = st.columns(5)

with col_a:
    nacht = st.slider("Nacht (0u–6u)", 14, 22, 17)
with col_b:
    ochtend = st.slider("Ochtend (6u–9u)", 14, 23, 20)
with col_c:
    voormiddag = st.slider("Voormiddag (9u–12u)", 14, 23, 19)
with col_d:
    namiddag = st.slider("Namiddag (12u–17u)", 14, 23, 19)
with col_e:
    avond = st.slider("Avond (17u–23u)", 14, 23, 21)

# 🔄 Dagcurve opbouwen op basis van dagdelen
dagcurve = []
for uur in range(24):
    if 0 <= uur < 6:
        dagcurve.append(nacht)
    elif 6 <= uur < 9:
        dagcurve.append(ochtend)
    elif 9 <= uur < 12:
        dagcurve.append(voormiddag)
    elif 12 <= uur < 17:
        dagcurve.append(namiddag)
    else:
        dagcurve.append(avond)

# 🔘 Simulatie starten
if st.button("🔍 Simuleer energieverbruik"):

    # 🌡️ Simpele buitentemperatuur (winterdag)
    buitentemp = [3 if 8 <= h <= 20 else 0 for h in range(24)]

    # 🔢 Instellen van verbruiksfactoren
    isolatiefactor = {"Slecht": 1.5, "Matig": 1.0, "Goed": 0.6}[isolatie]
    gedragfactor = {"Zuinig": 0.9, "Gemiddeld": 1.0, "Royaal": 1.2}[gedrag]

    # ⚡ Berekening verbruik per uur
    verbruik_per_uur = []
    for i in range(24):
        delta = max(0, dagcurve[i] - buitentemp[i])
        verbruik = delta * oppervlakte * 0.0005 * isolatiefactor * gedragfactor
        verbruik_per_uur.append(verbruik)

    totaal_kwh_per_dag = sum(verbruik_per_uur)
    jaarverbruik = totaal_kwh_per_dag * 365

    # ⚖️ Gemiddeld jaarverbruik per woningtype
    gemiddeld_per_type = {
        "Appartement": 9500,
        "Rijwoning": 11500,
        "Halfopen woning": 14500,
        "Vrijstaande woning": 22000
    }
    gemiddeld_verbruik = gemiddeld_per_type[woningtype]

    st.success(f"💡 Geschat dagelijks verbruik: **{totaal_kwh_per_dag:.2f} kWh**")
    st.info(f"📆 Geschat jaarlijks verbruik: **{jaarverbruik:.0f} kWh**")
    st.markdown(f"⚖️ Gemiddeld jaarverbruik voor een {woningtype.lower()} in Vlaanderen: **{gemiddeld_verbruik} kWh**")

    # 📊 Dataframe + grafieken
    df = pd.DataFrame({
        "Uur": list(range(24)),
        "BinnenT (°C)": dagcurve,
        "BuitenT (°C)": buitentemp,
        "Verbruik (kWh)": verbruik_per_uur
    })

    st.line_chart(df.set_index("Uur")[["BinnenT (°C)", "BuitenT (°C)"]])
    st.bar_chart(df.set_index("Uur")[["Verbruik (kWh)"]])
