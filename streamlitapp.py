import streamlit as st
import pandas as pd
from sqlalchemy import create_engine,text

@st.cache_resource
def get_mysql_engine():
    username = "root"          
    password = "shoulderblade" 
    host = "localhost"         
    port = "3306"              
    database = "ola_ride_insights"   
    
    return create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

engine = get_mysql_engine()


st.markdown(
    "<h1 style='text-align: center;'>Ola Ride Insights</h1>", 
    unsafe_allow_html=True
)
#st.subheader("based on the Chicago Traffic Crashes dataset (2020-2026)")

query_choice = st.selectbox("Select a query to view the results:", [
    "All Successful Bookings",
    "Average ride distance for each vehicle type",
    "Total number of cancelled rides by customers",
    "Top 5 customers who booked the highest number of rides",
    "Number of rides cancelled by drivers due to personal and car-related issues",
    "Maximum and Minimum driver ratings for Prime Sedan bookings",
    "All rides where payment was made using UPI",
    "Average customer rating per vehicle type",
    "The total booking value of rides completed successfully",
    "All incomplete rides along with the reason"
    
])

if query_choice == "All Successful Bookings":
    st.title("All Successful Bookings")
    query1 = """SELECT *
    FROM ola_ride_insights
    WHERE booking_status = 'Success'"""
    df1 = pd.read_sql_query(query1, con=engine)
    st.dataframe(df1, use_container_width=True)
    st.markdown(f"The table above shows all the {df1.shape[0]} successful bookings from the Ola Ride Insights dataset.")

if query_choice == "Average ride distance for each vehicle type":
    st.title("Average ride distance for each vehicle type")
    query2 = """SELECT
    vehicle_type,
    ROUND(AVG(ride_distance), 2) AS avg_ride_distance_km
    FROM ola_ride_insights
    WHERE booking_status = 'Success'
    GROUP BY vehicle_type
    ORDER BY avg_ride_distance_km DESC"""
    df2 = pd.read_sql_query(query2, con=engine)
    st.dataframe(df2, use_container_width=True)
    st.markdown("The table shows the average ride distance for each vehicle type.")

if query_choice == "Total number of cancelled rides by customers":
    st.title("Total number of cancelled rides by customers")
    query3 = """SELECT COUNT(*) AS cancelled_by_customer
    FROM ola_ride_insights
    WHERE booking_status = 'Canceled by Customer'"""
    df3 = pd.read_sql_query(query3, con=engine)
    total_cancelled = df3["cancelled_by_customer"].iloc[0]
    st.metric(label = "",value=f"{total_cancelled:}")
    #st.dataframe(df3, use_container_width=True)
    #st.markdown("The table shows the total number of cancelled rides by customers.")

if query_choice == "Top 5 customers who booked the highest number of rides":
    st.title("Top 5 customers who booked the highest number of rides")
    query4 = """SELECT
    customer_id,
    COUNT(*) AS total_rides,
    SUM(booking_value) AS total_booking_value
    FROM ola_ride_insights
    GROUP BY customer_id
    ORDER BY total_rides DESC, total_booking_value DESC
    LIMIT 5"""
    df4 = pd.read_sql_query(query4, con=engine)
    st.dataframe(df4, use_container_width=True)
    st.markdown("The table shows the top 5 customers who booked the highest number of rides.")

if query_choice == "Number of rides cancelled by drivers due to personal and car-related issues":
    st.title("Number of rides cancelled by drivers due to personal and car-related issues")
    query5 = """SELECT COUNT(*) AS driver_cancels_personal_car_issue
    FROM ola_ride_insights
    WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue'"""
    df5 = pd.read_sql_query(query5, con=engine)
    total_cancelled_by_driver = df5["driver_cancels_personal_car_issue"].iloc[0]
    st.metric(label = "",value=f"{total_cancelled_by_driver:}")
    #st.dataframe(df5, use_container_width=True)
    #st.markdown("The table shows the total number of cancelled rides by drivers due to personal and car-related issues.")


if query_choice == "Maximum and Minimum driver ratings for Prime Sedan bookings":
    st.title("Maximum and Minimum driver ratings for Prime Sedan bookings")
    query6 = """SELECT
    MAX(Driver_Ratings) AS max_driver_rating,
    MIN(Driver_Ratings) AS min_driver_rating
    FROM ola_ride_insights
    WHERE Vehicle_Type = 'Prime Sedan'
    AND booking_status = 'Success'"""
    df6 = pd.read_sql_query(query6, con=engine)
    maxi = df6["max_driver_rating"].iloc[0]
    mini = df6["min_driver_rating"].iloc[0]
    st.metric(label = "Maximum Driver Rating",value=f"{maxi:}")
    st.metric(label = "Minimum Driver Rating",value=f"{mini:}")
    #st.dataframe(df6, use_container_width=True)
    #st.markdown("The table shows the Maximum and Minimum driver ratings for Prime Sedan bookings.")

if query_choice == "All rides where payment was made using UPI":
    st.title("All rides where payment was made using UPI")
    query7 = """SELECT *
    FROM ola_ride_insights
    WHERE Payment_Method = 'UPI'"""
    df7 = pd.read_sql_query(query7, con=engine)
    st.dataframe(df7, use_container_width=True)
    st.markdown(f"The table shows all rides where the payment was made using UPI. There were totally {df7.shape[0]} rides where payment was made using UPI.")


if query_choice == "Average customer rating per vehicle type":
    st.title("Average customer rating per vehicle type")
    query8 = """SELECT
    Vehicle_Type,
    ROUND(AVG(Customer_Rating), 2) AS avg_customer_rating
    FROM ola_ride_insights
    GROUP BY Vehicle_Type
    ORDER BY avg_customer_rating DESC"""
    df8 = pd.read_sql_query(query8, con=engine)
    st.dataframe(df8, use_container_width=True)
    st.markdown("The table shows the average customer rating per vehicle type.")


if query_choice == "The total booking value of rides completed successfully":
    st.title("The total booking value of rides completed successfully")
    query9 = """SELECT SUM(Booking_Value) AS total_booking_value
    FROM ola_ride_insights
    WHERE Booking_Status = 'Success'"""
    df9 = pd.read_sql_query(query9, con=engine)
    successbkvalue = df9["total_booking_value"].iloc[0]
    st.metric(label = "", value = f"{successbkvalue:,}")
    #st.dataframe(df9, use_container_width=True)
    #st.markdown("The table shows the total booking value of rides completed successfully.")


if query_choice == "All incomplete rides along with the reason":
    st.title("All incomplete rides along with the reason")
    query10 = """SELECT
    Booking_ID,
    Date,
    Vehicle_Type,
    Pickup_Location,
    Drop_Location,
    Incomplete_Rides_Reason
    FROM ola_ride_insights
    WHERE Incomplete_Rides = 'Yes'
    ORDER BY Date, Booking_ID"""
    df10 = pd.read_sql_query(query10, con=engine)
    st.dataframe(df10, use_container_width=True)
    st.markdown(f"This table shows all incomplete rides along with the reason. There are totally {df10.shape[0]} incomplete rides.")
