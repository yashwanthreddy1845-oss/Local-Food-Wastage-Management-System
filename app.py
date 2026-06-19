import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

st.set_page_config(
    page_title="Local Food Wastage Management System",
    page_icon="🍔",
    layout="wide"
)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yash45",
    database="food_wastage"
)

menu = st.sidebar.selectbox(
    "Menu",
    [
    "Home",
    "Providers",
    "Food Listings",
    "Receivers",
    "Filters",
    "SQL Dashboard",
    "Add Food",
    "Update Food",
    "Delete Food"
]
)

# ---------------- HOME ---------------- #

if menu == "Home":

    st.title("🍔 Local Food Wastage Management System")

    providers_count = pd.read_sql(
        "SELECT COUNT(*) AS total FROM providers",
        conn
    ).iloc[0, 0]

    receivers_count = pd.read_sql(
        "SELECT COUNT(*) AS total FROM receivers",
        conn
    ).iloc[0, 0]

    listings_count = pd.read_sql(
        "SELECT COUNT(*) AS total FROM food_listings",
        conn
    ).iloc[0, 0]

    claims_count = pd.read_sql(
        "SELECT COUNT(*) AS total FROM claims",
        conn
    ).iloc[0, 0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Providers", providers_count)
    col2.metric("Receivers", receivers_count)
    col3.metric("Food Listings", listings_count)
    col4.metric("Claims", claims_count)

    st.markdown("---")

    st.subheader("📊 Project Overview")

    st.write("""
    This platform helps reduce food wastage by connecting food providers
    with receivers and enabling food redistribution.
    """)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        meal_df = pd.read_sql("""
        SELECT Meal_Type,
               COUNT(*) AS Total_Count
        FROM food_listings
        GROUP BY Meal_Type
        """, conn)

        fig1 = px.pie(
            meal_df,
            names="Meal_Type",
            values="Total_Count",
            title="Meal Type Distribution"
        )

        st.plotly_chart(fig1, use_container_width=True)

    with chart_col2:

        food_df = pd.read_sql("""
        SELECT Food_Type,
               COUNT(*) AS Total_Count
        FROM food_listings
        GROUP BY Food_Type
        """, conn)

        fig2 = px.bar(
            food_df,
            x="Food_Type",
            y="Total_Count",
            title="Food Type Distribution"
        )

        st.plotly_chart(fig2, use_container_width=True)

    provider_df = pd.read_sql("""
    SELECT Provider_Type,
           SUM(Quantity) AS Total_Food
    FROM food_listings
    GROUP BY Provider_Type
    """, conn)

    fig3 = px.bar(
        provider_df,
        x="Provider_Type",
        y="Total_Food",
        title="Food Quantity by Provider Type"
    )

    st.plotly_chart(fig3, use_container_width=True)

    location_df = pd.read_sql("""
    SELECT Location,
           SUM(Quantity) AS Total_Food
    FROM food_listings
    GROUP BY Location
    ORDER BY Total_Food DESC
    LIMIT 10
    """, conn)

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

    df = pd.read_sql(
        "SELECT * FROM providers",
        conn
    )

    st.dataframe(df)

# ---------------- FOOD LISTINGS ---------------- #

elif menu == "Food Listings":

    st.title("Food Listings")

    df = pd.read_sql(
        "SELECT * FROM food_listings",
        conn
    )

    st.dataframe(df)

# ---------------- RECEIVERS ---------------- #

elif menu == "Receivers":

    st.title("Receivers Data")

    df = pd.read_sql(
        "SELECT * FROM receivers",
        conn
    )

    st.dataframe(df)

# ---------------- FILTERS ---------------- #

elif menu == "Filters":

    st.title("Filters")

    df = pd.read_sql(
        "SELECT * FROM food_listings",
        conn
    )

    city_list = ["All"] + sorted(
        df["Location"].dropna().unique().tolist()
    )

    provider_list = ["All"] + sorted(
        df["Provider_Type"].dropna().unique().tolist()
    )

    food_list = ["All"] + sorted(
        df["Food_Type"].dropna().unique().tolist()
    )

    meal_list = ["All"] + sorted(
        df["Meal_Type"].dropna().unique().tolist()
    )

    selected_city = st.selectbox(
        "Select City",
        city_list
    )

    selected_provider = st.selectbox(
        "Select Provider Type",
        provider_list
    )

    selected_food = st.selectbox(
        "Select Food Type",
        food_list
    )

    selected_meal = st.selectbox(
        "Select Meal Type",
        meal_list
    )

    filtered_df = df.copy()

    if selected_city != "All":
        filtered_df = filtered_df[
            filtered_df["Location"] == selected_city
        ]

    if selected_provider != "All":
        filtered_df = filtered_df[
            filtered_df["Provider_Type"] == selected_provider
        ]

    if selected_food != "All":
        filtered_df = filtered_df[
            filtered_df["Food_Type"] == selected_food
        ]

    if selected_meal != "All":
        filtered_df = filtered_df[
            filtered_df["Meal_Type"] == selected_meal
        ]

    st.dataframe(filtered_df)
# ---------------- SQL DASHBOARD ---------------- #

elif menu == "SQL Dashboard":

    st.title("SQL Dashboard")

    queries = [
        ("1. Total Food Available",
         "SELECT SUM(Quantity) AS Total_Food_Available FROM food_listings"),

        ("2. Food Listings by Location",
         """SELECT Location, COUNT(*) AS Total_Listings
            FROM food_listings
            GROUP BY Location
            ORDER BY Total_Listings DESC"""),

        ("3. Food Type Distribution",
         """SELECT Food_Type, COUNT(*) AS Count_Food
            FROM food_listings
            GROUP BY Food_Type
            ORDER BY Count_Food DESC"""),

        ("4. Provider Type Contribution",
         """SELECT Provider_Type, SUM(Quantity) AS Total_Food
            FROM food_listings
            GROUP BY Provider_Type
            ORDER BY Total_Food DESC"""),

        ("5. Providers by City",
         """SELECT City, COUNT(*) AS Total_Providers
            FROM providers
            GROUP BY City
            ORDER BY Total_Providers DESC"""),

        ("6. Receivers by City",
         """SELECT City, COUNT(*) AS Total_Receivers
            FROM receivers
            GROUP BY City
            ORDER BY Total_Receivers DESC"""),

        ("7. Providers List",
         """SELECT Name, Contact, City
            FROM providers
            ORDER BY City"""),

        ("8. Top Receivers by Claims",
         """SELECT r.Receiver_ID, r.Name,
            COUNT(c.Claim_ID) AS Total_Claims
            FROM receivers r
            JOIN claims c
            ON r.Receiver_ID = c.Receiver_ID
            GROUP BY r.Receiver_ID, r.Name
            ORDER BY Total_Claims DESC"""),

        ("9. Most Claimed Food Items",
         """SELECT Food_ID,
            COUNT(*) AS Total_Claims
            FROM claims
            GROUP BY Food_ID
            ORDER BY Total_Claims DESC"""),

        ("10. Providers with Successful Claims",
         """SELECT p.Provider_ID,p.Name,
            COUNT(c.Claim_ID) AS Successful_Claims
            FROM providers p
            JOIN food_listings f
            ON p.Provider_ID=f.Provider_ID
            JOIN claims c
            ON f.Food_ID=c.Food_ID
            WHERE c.Status='Completed'
            GROUP BY p.Provider_ID,p.Name
            ORDER BY Successful_Claims DESC"""),

        ("11. Average Food Quantity",
         """SELECT AVG(Quantity) AS Avg_Quantity
            FROM food_listings"""),

        ("12. Meal Type Distribution",
         """SELECT Meal_Type,
            COUNT(*) AS Total_Count
            FROM food_listings
            GROUP BY Meal_Type
            ORDER BY Total_Count DESC"""),

        ("13. Top Providers by Food Donation",
         """SELECT Provider_ID,
            SUM(Quantity) AS Total_Donated
            FROM food_listings
            GROUP BY Provider_ID
            ORDER BY Total_Donated DESC"""),

        ("14. Top 10 Locations by Food Quantity",
         """SELECT Location,
            SUM(Quantity) AS Total_Food
            FROM food_listings
            GROUP BY Location
            ORDER BY Total_Food DESC
            LIMIT 10"""),

        ("15. Provider Type Performance",
         """SELECT Provider_Type,
            COUNT(*) AS Total_Listings,
            SUM(Quantity) AS Total_Food
            FROM food_listings
            GROUP BY Provider_Type
            ORDER BY Total_Food DESC""")
    ]

    for title, query in queries:
        st.subheader(title)
        st.dataframe(pd.read_sql(query, conn))
        # ---------------- ADD FOOD ---------------- #

elif menu == "Add Food":

    st.title("Add Food Listing")

    food_name = st.text_input("Food Name")
    quantity = st.number_input("Quantity", min_value=1)
    expiry_date = st.date_input("Expiry Date")
    provider_id = st.number_input("Provider ID", min_value=1)
    provider_type = st.text_input("Provider Type")
    location = st.text_input("Location")

    food_type = st.selectbox(
        "Food Type",
        ["Vegetarian", "Non-Vegetarian", "Vegan"]
    )

    meal_type = st.selectbox(
        "Meal Type",
        ["Breakfast", "Lunch", "Dinner", "Snacks"]
    )

    if st.button("Add Food"):

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO food_listings
        (
            Food_Name,
            Quantity,
            Expiry_Date,
            Provider_ID,
            Provider_Type,
            Location,
            Food_Type,
            Meal_Type
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            food_name,
            quantity,
            expiry_date,
            provider_id,
            provider_type,
            location,
            food_type,
            meal_type
        ))

        conn.commit()

        st.success("Food Listing Added Successfully")


# ---------------- UPDATE FOOD ---------------- #

elif menu == "Update Food":

    st.title("Update Food Quantity")

    food_id = st.number_input(
        "Enter Food ID",
        min_value=1
    )

    new_quantity = st.number_input(
        "New Quantity",
        min_value=1
    )

    if st.button("Update Food"):

        cursor = conn.cursor()

        cursor.execute("""
        UPDATE food_listings
        SET Quantity=%s
        WHERE Food_ID=%s
        """,
        (
            new_quantity,
            food_id
        ))

        conn.commit()

        st.success("Food Listing Updated Successfully")


# ---------------- DELETE FOOD ---------------- #

elif menu == "Delete Food":

    st.title("Delete Food Listing")

    food_id = st.number_input(
        "Enter Food ID To Delete",
        min_value=1
    )

    if st.button("Delete Food"):

        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM food_listings
        WHERE Food_ID=%s
        """,
        (food_id,)
        )

        conn.commit()

        st.success("Food Listing Deleted Successfully")

conn.close()