import plotly.graph_objects as go
import streamlit as st

from gas_calculator.calculator import (
    build_estimates,
    estimate_distance_to_empty,
    to_gallons,
    to_liters,
)

US_PRESETS = {
    "Compact Car": 12.0,
    "Sedan": 15.0,
    "SUV": 18.0,
    "Truck": 26.0,
}

METRIC_PRESETS = {
    "Compact Car": 45.0,
    "Sedan": 57.0,
    "SUV": 68.0,
    "Truck": 98.0,
}


def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"


def format_volume(amount: float, unit: str) -> str:
    return f"{amount:,.2f} {unit}"


def gauge_color(percent: float) -> str:
    if percent < 20:
        return "#b80f1a"
    if percent < 50:
        return "#d97706"
    return "#15803d"


def seed_profiles() -> None:
    if "vehicle_profiles" in st.session_state:
        return

    st.session_state.vehicle_profiles = {
        "US": {
            name: {
                "name": name,
                "capacity": capacity,
                "efficiency": 28.0,
            }
            for name, capacity in US_PRESETS.items()
        },
        "Metric": {
            name: {
                "name": name,
                "capacity": capacity,
                "efficiency": 12.0,
            }
            for name, capacity in METRIC_PRESETS.items()
        },
    }


def reset_profiles(unit_system: str) -> None:
    defaults = US_PRESETS if unit_system == "US" else METRIC_PRESETS
    st.session_state.vehicle_profiles[unit_system] = {
        name: {
            "name": name,
            "capacity": capacity,
            "efficiency": 28.0 if unit_system == "US" else 12.0,
        }
        for name, capacity in defaults.items()
    }


def render_style() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Source+Code+Pro:wght@400;600&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Space Grotesk', sans-serif;
        }
        .stApp {
            background: radial-gradient(circle at 20% 20%, #fef3c7 0%, #ffffff 45%, #ecfeff 100%);
        }
        h1, h2, h3 {
            letter-spacing: -0.02em;
        }
        .section-card {
            padding: 1.2rem 1.4rem;
            border-radius: 18px;
            background: #ffffff;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
            border: 1px solid #e2e8f0;
        }
        .subtle {
            color: #475569;
            font-size: 0.95rem;
        }
        .kicker {
            text-transform: uppercase;
            letter-spacing: 0.15em;
            font-size: 0.7rem;
            color: #64748b;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def profile_controls(
    unit_system: str, volume_unit: str, efficiency_unit: str
) -> tuple[float, float]:
    profiles = st.session_state.vehicle_profiles[unit_system]
    profile_names = ["Custom"] + sorted(profiles.keys())

    st.subheader("Vehicle Profile")
    selected_profile_key = f"profile_{unit_system}"
    selected_profile = st.selectbox("Profile", options=profile_names, key=selected_profile_key)

    capacity_key = f"capacity_{unit_system}"
    efficiency_key = f"efficiency_{unit_system}"
    prev_profile_key = f"profile_prev_{unit_system}"

    if selected_profile != "Custom":
        profile = profiles[selected_profile]
        default_capacity = profile["capacity"]
        default_efficiency = profile["efficiency"]
    else:
        default_capacity = (
            METRIC_PRESETS["Sedan"] if unit_system == "Metric" else US_PRESETS["Sedan"]
        )
        default_efficiency = 12.0 if unit_system == "Metric" else 28.0

    if prev_profile_key not in st.session_state:
        st.session_state[prev_profile_key] = selected_profile
    if st.session_state[prev_profile_key] != selected_profile:
        st.session_state[capacity_key] = float(default_capacity)
        st.session_state[efficiency_key] = float(default_efficiency)
        st.session_state[prev_profile_key] = selected_profile

    capacity = st.number_input(
        f"Tank capacity ({volume_unit})",
        min_value=0.1,
        value=float(default_capacity),
        step=0.1,
        key=capacity_key,
    )
    efficiency = st.number_input(
        f"Fuel efficiency ({efficiency_unit})",
        min_value=0.1,
        value=float(default_efficiency),
        step=0.1,
        help="Used to estimate remaining range.",
        key=efficiency_key,
    )

    st.markdown("<div class='kicker'>Save profile</div>", unsafe_allow_html=True)
    profile_name = st.text_input("Profile name", value="", key=f"profile_name_{unit_system}")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Save", use_container_width=True, disabled=profile_name.strip() == ""):
            trimmed_name = profile_name.strip()
            profiles[trimmed_name] = {
                "name": trimmed_name,
                "capacity": float(capacity),
                "efficiency": float(efficiency),
            }
            st.session_state[selected_profile_key] = trimmed_name
            st.success("Profile saved.")
    with col_b:
        delete_disabled = selected_profile in ("Custom",)
        if st.button("Delete", use_container_width=True, disabled=delete_disabled):
            profiles.pop(selected_profile, None)
            st.session_state[selected_profile_key] = "Custom"
            st.info("Profile deleted.")

    return float(capacity), float(efficiency)


def run_app() -> None:
    st.set_page_config(page_title="Gas Tank Calculator", layout="wide")
    render_style()
    seed_profiles()

    st.markdown("<div class='kicker'>Fuel planning</div>", unsafe_allow_html=True)
    st.title("Gas Tank Calculator")
    st.markdown(
        """
        <div class='subtle'>
            Estimate fill-up costs, remaining range, and top-up targets.
            Configure multiple vehicles and switch between them anytime.
        </div>
        """,
        unsafe_allow_html=True,
    )

    unit_system = st.radio("Unit system", ("US", "Metric"), horizontal=True)
    is_metric = unit_system == "Metric"

    volume_unit = "L" if is_metric else "gal"
    efficiency_unit = "km/L" if is_metric else "mpg"

    with st.sidebar:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("Fuel Inputs")
        if st.button("Reset profiles", use_container_width=True):
            reset_profiles(unit_system)
        price = st.number_input(
            f"Fuel price per {volume_unit}",
            min_value=0.01,
            value=3.50,
            step=0.01,
            format="%.2f",
        )
        capacity, efficiency = profile_controls(unit_system, volume_unit, efficiency_unit)
        st.markdown("</div>", unsafe_allow_html=True)

    left, right = st.columns([1.05, 1])
    current_level_key = f"current_level_{unit_system}"
    if current_level_key not in st.session_state:
        st.session_state[current_level_key] = float(capacity / 2.0)
    if st.session_state[current_level_key] > float(capacity):
        st.session_state[current_level_key] = float(capacity)

    with left:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("Current Fuel Level")
        current_level = st.slider(
            f"Current fuel level ({volume_unit})",
            min_value=0.0,
            max_value=float(capacity),
            value=float(st.session_state[current_level_key]),
            step=0.1,
            key=current_level_key,
        )

        quick_cols = st.columns(4)
        quick_points = [("25%", 0.25), ("50%", 0.50), ("75%", 0.75), ("Full", 1.0)]
        for col, (label, ratio) in zip(quick_cols, quick_points, strict=False):
            with col:
                if st.button(label, use_container_width=True, key=f"quick_{label}_{unit_system}"):
                    st.session_state[current_level_key] = float(capacity * ratio)

        st.markdown("</div>", unsafe_allow_html=True)

    try:
        estimates = build_estimates(
            price_per_unit=price,
            capacity=capacity,
            current_level=current_level,
        )
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    with right:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=estimates.current_percent,
                title={"text": "Tank Level"},
                number={"suffix": "%"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": gauge_color(estimates.current_percent)},
                    "steps": [
                        {"range": [0, 20], "color": "#fee2e2"},
                        {"range": [20, 50], "color": "#fde68a"},
                        {"range": [50, 100], "color": "#dcfce7"},
                    ],
                },
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Fill-Up Summary")
    summary_cols = st.columns(3)
    summary_cols[0].metric("Fuel needed", format_volume(estimates.needed, volume_unit))
    summary_cols[1].metric("Cost to full", format_currency(estimates.total_cost))
    range_to_empty = estimate_distance_to_empty(current_level=current_level, efficiency=efficiency)
    summary_cols[2].metric(
        "Estimated range",
        f"{range_to_empty:,.1f} {efficiency_unit.split('/')[0]}",
    )

    if is_metric:
        alt_needed = to_gallons(estimates.needed)
        st.caption(f"Equivalent volume: {alt_needed:,.2f} gal")
    else:
        alt_needed = to_liters(estimates.needed)
        st.caption(f"Equivalent volume: {alt_needed:,.2f} L")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Top-Up Cost Targets")
    c1, c2, c3 = st.columns(3)
    c1.metric("To 1/4 tank", format_currency(estimates.cost_to_quarter))
    c2.metric("To 1/2 tank", format_currency(estimates.cost_to_half))
    c3.metric("To full tank", format_currency(estimates.cost_to_full))
    st.markdown("</div>", unsafe_allow_html=True)
