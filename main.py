import streamlit as st
import plotly.graph_objects as go

st.title("Gas Tank Calculator")

# create input fields for price, capacity, and current level
price_type = st.radio("Price type", ("Per liter","Per gallon"))
if price_type == "Per gallon":
    price = st.number_input("Price per gallon")
else:
    price = st.number_input("Price per liter")

tank_capacity = st.number_input("Tank capacity (in gallons)", value=11, step=1)
current_gas_level = st.slider("Current gas level (in gallons)", 0.0, float(tank_capacity), float(tank_capacity / 2.0), 0.1)

# calculate how many gallons are needed to fill up the tank
gallons_needed = tank_capacity - current_gas_level

# calculate the total cost to fill up the tank
if price_type == "Per liter":
    price_per_gallon = price * 3.78541  # Convert price from liter to gallon
else:
    price_per_gallon = price

total_cost = round(price_per_gallon * gallons_needed, 2)

# create gauge figure to display current gas level
fig = go.Figure(go.Indicator(
    mode="gauge",
    value=current_gas_level,
    title={'text': "Current Gas Level"},
    domain={'x': [0, 1], 'y': [0, 1]},
    gauge={
        'axis': {'visible': False, 'range': [0, tank_capacity]},
        'bar': {'color': "red"},
        'steps': [
            {'range': [0, tank_capacity], 'color': "lightgray"}
        ],
    }))

# display the gauge figure and the gas tank calculator results
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.write("To fill up your gas tank:")
    st.write("- You need to add", gallons_needed, "gallons")
    st.write("- The total cost will be $", total_cost)
