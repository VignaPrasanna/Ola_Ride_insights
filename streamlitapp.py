import streamlit as st
import pandas as pd
import duckdb
#from sqlalchemy import create_engine,text

@st.cache_resource
def get_db_connection():
  # Connects to an in-memory DuckDB instance and registers your CSV as a table named 'ola_rides'
  con = duckdb.connect(database=":memory:", read_only=False)
  # Read the CSV using pandas and register it as a virtual SQL table
  df = pd.read_csv("ola_ride_insights_dataset.csv", sep=";")
  df.columns = df.columns.str.strip()
  con.register("ola_rides", df)
  return con


con = get_db_connection()

df = con.execute("SELECT * FROM ola_rides").df()
#def get_mysql_engine():
#    username = "root"          
#    password = "shoulderblade" 
#    host = "localhost"         
#    port = "3306"              
#    database = "ola_ride_insights"   
    
#    return create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

#engine = get_mysql_engine()


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
#st.write(df.columns.tolist())
if query_choice == "All Successful Bookings":
  st.title("All Successful Bookings")
  df1 = df[df["Booking_Status"] == "Success"]  # Check exact column casing
  st.dataframe(df1, use_container_width=True)
  st.markdown(
      f"The table above shows all the {df1.shape[0]} successful bookings from"
      " the Ola Ride Insights dataset."
  )

elif query_choice == "Average ride distance for each vehicle type":
  st.title("Average ride distance for each vehicle type")
  df2 = (
      df[df["Booking_Status"] == "Success"]
      .groupby("Vehicle_Type")["Ride_Distance"]
      .mean()
      .round(2)
      .reset_index(name="avg_ride_distance_km")
  )
  df2 = df2.sort_values(by="avg_ride_distance_km", ascending=False)
  st.dataframe(df2, use_container_width=True)
  st.markdown("The table shows the average ride distance for each vehicle type.")

elif query_choice == "Total number of cancelled rides by customers":
  st.title("Total number of cancelled rides by customers")
  total_cancelled = len(df[df["Booking_Status"] == "Canceled by Customer"])
  st.metric(label="", value=f"{total_cancelled}")

elif query_choice == "Top 5 customers who booked the highest number of rides":
  st.title("Top 5 customers who booked the highest number of rides")
  df4 = (
      df.groupby("Customer_ID")
      .agg(total_rides=("Booking_ID", "count"), total_booking_value=("Booking_Value", "sum"))
      .reset_index()
      .sort_values(by=["total_rides", "total_booking_value"], ascending=False)
      .head(5)
  )
  st.dataframe(df4, use_container_width=True)
  st.markdown("The table shows the top 5 customers who booked the highest number of rides.")

elif query_choice == "Number of rides cancelled by drivers due to personal and car-related issues":
  st.title("Number of rides cancelled by drivers due to personal and car-related issues")
  total_cancelled_by_driver = len(
      df[df["Canceled_Rides_by_Driver"] == "Personal & Car related issue"]
  )
  st.metric(label="", value=f"{total_cancelled_by_driver}")

elif query_choice == "Maximum and Minimum driver ratings for Prime Sedan bookings":
  st.title("Maximum and Minimum driver ratings for Prime Sedan bookings")
  prime_sedan = df[(df["Vehicle_Type"] == "Prime Sedan") & (df["Booking_Status"] == "Success")]
  maxi = prime_sedan["Driver_Ratings"].max()
  mini = prime_sedan["Driver_Ratings"].min()
  st.metric(label="Maximum Driver Rating", value=f"{maxi}")
  st.metric(label="Minimum Driver Rating", value=f"{mini}")

elif query_choice == "All rides where payment was made using UPI":
  st.title("All rides where payment was made using UPI")
  df7 = df[df["Payment_Method"] == "UPI"]
  st.dataframe(df7, use_container_width=True)
  st.markdown(
      f"The table shows all rides where the payment was made using UPI. There"
      f" were totally {df7.shape[0]} rides where payment was made using UPI."
  )

elif query_choice == "Average customer rating per vehicle type":
  st.title("Average customer rating per vehicle type")
  df8 = (
      df.groupby("Vehicle_Type")["Customer_Rating"]
      .mean()
      .round(2)
      .reset_index(name="avg_customer_rating")
      .sort_values(by="avg_customer_rating", ascending=False)
  )
  st.dataframe(df8, use_container_width=True)
  st.markdown("The table shows the average customer rating per vehicle type.")

elif query_choice == "The total booking value of rides completed successfully":
  st.title("The total booking value of rides completed successfully")
  successbkvalue = df[df["Booking_Status"] == "Success"]["Booking_Value"].sum()
  st.metric(label="", value=f"{successbkvalue:,.2f}")

elif query_choice == "All incomplete rides along with the reason":
  st.title("All incomplete rides along with the reason")
  df10 = df[df["Incomplete_Rides"] == "Yes"][
      ["Booking_ID", "Date", "Vehicle_Type", "Pickup_Location", "Drop_Location", "Incomplete_Rides_Reason"]
  ].sort_values(by=["Date", "Booking_ID"])
  st.dataframe(df10, use_container_width=True)
  st.markdown(
      f"This table shows all incomplete rides along with the reason. There are"
      f" totally {df10.shape[0]} incomplete rides."
  )
