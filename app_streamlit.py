import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Local Food Wastage Management System",
    page_icon="🍔",
    layout="wide"
)

# Load CSV Files
providers = pd.read_csv("providers_data_utf8.csv")
receivers = pd.read_csv("receivers_data_utf8.csv")
food_listings = pd.read_csv("food_listings_data_utf8.csv")
claims = pd.read_csv("claims_data_utf8.csv")

# Sidebar Menu
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Home",
        "Providers",
        "Food Listings",
        "Receivers",
        "Filters"
    ]
)

# ---------------- HOME ---------------- #

if menu == "Home":

    st.title("🍔 Local Food Wastage Management System")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Providers", len(providers))
    col2.metric("Receivers", len(receivers))
    col3.metric("Food Listings", len(food_listings))
    col4.metric("Claims", len(claims))

    st.markdown("---")

    st.subheader("📊 Project Overview")

    st.write("""
    This platform helps reduce food wastage by connecting food providers
    with receivers and enabling efficient food redistribution.
    """)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        meal_df = (
            food_listings.groupby("Meal_Type")
            .size()
            .reset_index(name="Total_Count")
        )

        fig1 = px.pie(
            meal_df,
            names="Meal_Type",
            values="Total_Count",
            title="Meal Type Distribution"
        )

        st.plotly_chart(fig1, use_container_width=True)

    with chart_col2:

        food_df = (
            food_listings.groupby("Food_Type")
            .size()
            .reset_index(name="Total_Count")
        )

        fig2 = px.bar(
            food_df,
            x="Food_Type",
            y="Total_Count",
            title="Food Type Distribution"
        )

        st.plotly_chart(fig2, use_container_width=True)

    provider_df = (
        food_listings.groupby("Provider_Type")["Quantity"]
        .sum()
        .reset_index(name="Total_Food")
    )

    fig3 = px.bar(
        provider_df,
        x="Provider_Type",
        y="Total_Food",
        title="Food Quantity by Provider Type"
    )

    st.plotly_chart(fig3, use_container_width=True)

    location_df = (
        food_listings.groupby("Location")["Quantity"]
        .sum()
        .reset_index(name="Total_Food")
        .sort_values("Total_Food", ascending=False)
        .head(10)
    )

    fig4 = px.bar(
        location_df,
        x="Location",
        y="Total_Food",
        title="Top 10 Locations by Food Quantity"
    )

    st.plotly_chart(fig4, use_container_width=True)

# ---------------- PROVIDERS ---------------- #

elif menu == "Providers":

    st.title("Providers Data")
    st.dataframe(providers)

# ---------------- FOOD LISTINGS ---------------- #

elif menu == "Food Listings":

    st.title("Food Listings")
    st.dataframe(food_listings)

# ---------------- RECEIVERS ---------------- #

elif menu == "Receivers":

    st.title("Receivers Data")
    st.dataframe(receivers)

# ---------------- FILTERS ---------------- #

elif menu == "Filters":

    st.title("Filters")

    city = st.selectbox(
        "Select City",
        ["All"] + sorted(food_listings["Location"].dropna().unique())
    )

    provider_type = st.selectbox(
        "Select Provider Type",
        ["All"] + sorted(food_listings["Provider_Type"].dropna().unique())
    )

    food_type = st.selectbox(
        "Select Food Type",
        ["All"] + sorted(food_listings["Food_Type"].dropna().unique())
    )

    meal_type = st.selectbox(
        "Select Meal Type",
        ["All"] + sorted(food_listings["Meal_Type"].dropna().unique())
    )

    filtered = food_listings.copy()

    if city != "All":
        filtered = filtered[
            filtered["Location"] == city
        ]

    if provider_type != "All":
        filtered = filtered[
            filtered["Provider_Type"] == provider_type
        ]

    if food_type != "All":
        filtered = filtered[
            filtered["Food_Type"] == food_type
        ]

    if meal_type != "All":
        filtered = filtered[
            filtered["Meal_Type"] == meal_type
        ]

    st.dataframe(filtered)