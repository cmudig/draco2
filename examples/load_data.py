import draco.data
import draco.run
import streamlit as st
from vega_datasets import data

st.title("Load Data")

df = data.seattle_weather()

st.write(df)

facts = draco.data.df_to_facts(df)

draco.run.run(facts=facts, models=3)
