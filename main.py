import plotly.graph_objects as go
import streamlit as st

from calculator import (
    build_estimates,
    estimate_distance_to_empty,
    to_gallons,
    to_liters,
)

US_PRESETS = {
    "Compact Car (12 gal)": 12.0,
    "Sedan (15 gal)": 15.0,
    "SUV (18 gal)": 18.0,
    "Truck (26 gal)": 26.0,
}

METRIC_PRESETS = {
    "Compact Car (45 L)": 45.0,
    "Sedan (57 L)": 57.0,
    "SUV (68 L)": 68.0,
    "Truck (98 L)": 98.0,
}


def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"


def format_volume(amount: float, unit: str) -> str:
    return f"{amount:,.2f} {unit}"


def gauge_color(percent: float) -> str:
    if percent < 20:
        return "#d90429"
    if percent < 50:
        return "#f77f00"
    return "#2b9348"


def main() -> None:
    st.set_page_config(page_title="Gas Tank Calculator", layout="wide")
    st.title("Gas Tank Calculator")
    st.caption("Estimate fill-up costs, fuel needed, and driving range from your current level.")

    unit_system = st.radio("Unit system", ("US", "Metric"), horizontal=True)
    is_metric = unit_system == "Metric"

    volume_unit = "L" if is_metric else "gal"
    efficiency_unit = "km/L" if is_metric else "mpg"
    presets = METRIC_PRESETS if is_metric else US_PRESETS

    with st.sidebar:
        st.subheader("Inputs")
        preset_name = st.selectbox("Vehicle preset", options=list(presets.keys()))
        default_capacity = presets[preset_name]

        price = st.number_input(
            f"Fuel price per {volume_unit}",
            min_value=0.01,
            value=3.50,
            step=0.01,
            format="%.2f",
        )
        tank_capacity = st.number_input(
            f"Tank capacity ({volume_unit})",
            min_value=0.1,
            value=float(default_capacity),
            step=0.1,
        )
        current_level = st.slider(
            f"Current fuel level ({volume_unit})",
            min_value=0.0,
            max_value=float(tank_capacity),
            value=float(tank_capacity / 2.0),
            step=0.1,
        )
        efficiency = st.number_input(
            f"Fuel efficiency ({efficiency_unit})",
            min_value=0.1,
            value=28.0 if not is_metric else 12.0,
            step=0.1,
            help="Used to estimate remaining driving range.",
        )

    try:
        estimates = build_estimates(
            price_per_unit=price,
            capacity=tank_capacity,
            current_level=current_level,
        )
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    col1, col2 = st.columns([1, 1])

    with col1:
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=estimates.current_percent,
                title={"text": "Current Tank Level"},
                number={"suffix": "%"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": gauge_color(estimates.current_percent)},
                    "steps": [
                        {"range": [0, 20], "color": "#ffccd5"},
                        {"range": [20, 50], "color": "#ffe5b4"},
                        {"range": [50, 100], "color": "#d8f3dc"},
                    ],
                },
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Fill-Up Summary")
        st.metric("Fuel needed", format_volume(estimates.needed, volume_unit))
        st.metric("Cost to full", format_currency(estimates.total_cost))

        if is_metric:
            alt_needed = to_gallons(estimates.needed)
            st.caption(f"Equivalent: {alt_needed:,.2f} gal")
        else:
            alt_needed = to_liters(estimates.needed)
            st.caption(f"Equivalent: {alt_needed:,.2f} L")

        range_to_empty = estimate_distance_to_empty(
            current_level=current_level, efficiency=efficiency
        )
        st.metric(
            "Estimated range at current level",
            f"{range_to_empty:,.1f} {efficiency_unit.split('/')[0]}",
        )

    st.subheader("Top-Up Cost Targets")
    c1, c2, c3 = st.columns(3)
    c1.metric("To 1/4 tank", format_currency(estimates.cost_to_quarter))
    c2.metric("To 1/2 tank", format_currency(estimates.cost_to_half))
    c3.metric("To full tank", format_currency(estimates.cost_to_full))


if __name__ == "__main__":
    main()
