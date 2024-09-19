import streamlit as st
import pandas as pd
import plotly_express as px

# Import your EDA module
import notebooks.EDA as eda

# Load the data (this ensures the CSV is loaded, cleaned and processed)
load_message = eda.load_data()

# Display file path
# st.write("Source file path: ", eda.get_file_path())

# Include CSS styles within the <style> tag
st.markdown("""
    <style>
    h1 {
        color: green;
    }
    h4 {
        color: blue;
    }
    h6 {
        color: blue;
    }
    </style>
    """, unsafe_allow_html=True)


st.markdown("<h1>Vehicles Data Analysis</h1>", unsafe_allow_html=True)

# Show the data loading status
# st.write("Data Loading Status: ", load_message)
st.markdown(f"<b>Data Loading Status: </b>{load_message}", unsafe_allow_html=True)

# Display the DataFrame if data was loaded successfully
if load_message == "Data loaded successfully":
    # st.dataframe(eda.get_df()) # Render HTML content
    st.markdown("<h4>Displaying the first few lines of raw data csv data</h4>", unsafe_allow_html=True)
    # st.title("Confirmation that file has loaded")
    st.dataframe(eda.get_df_head())

    # Clean the data
    st.markdown("<h4>Cleaning the data ...</h4>", unsafe_allow_html=True)
    eda.cleanup_data()
    st.markdown("Having examined the csv data, the following steps were done:", unsafe_allow_html=True)

    # Describe how data was cleaned
    # Display the bullet point in a list
    st.markdown("""
        <ol>
            <li>Data was checked for duplicates and removed if necessary.</li>
            <li>Column 'is_4wd' was found to have '1' or missing values. This could be due to: (a) the data in its original format utilized 1 and 0 as boolean values, but the zeros were lost due to formatting and (b) that the data is truly missing. Considering that approximately one-half of this column has blank values, the former was chosen, and data was updated as follows: '1' was set to 'true' and missing values set to 'false'.</li>
            <li>Other rows containing blank values have been removed as they would have invalidated the accuracy of the query due to the presence of null or NaN values.</li>
            <li>Improved readability by capitalizing the first letter of each word related to vehicles.</li>
            <li>Modified 'model_year', 'cylinder' and 'odometer' to remove decimal places.</li>
            <li>Some rows with prices less than $300 were removed, as the condition of the vehicle was new, and the year and odometer value didn't seem to be correct. Other rows were removed because they seemed to be overpriced greater than $100,000 with very high mileage, and model_year was 15 years.</li>
        </ol>
        """, unsafe_allow_html=True)
    
    # Post cleanup of data
    st.markdown("<h6>Checking data following cleanup...</h6>", unsafe_allow_html=True)
    st.dataframe(eda.get_df_head())

    # Enhance the data
    st.markdown("<h4>Enhancing the data ...</h4>", unsafe_allow_html=True)
    # Check added column for manufacturer which will be used in subsequent analyses
    st.markdown("<h6>Adding column for manufacturer as this will be used in subsequent analyses</h6>", unsafe_allow_html=True)
    st.dataframe(eda.get_df_head())

    # Analyses
    eda.analyze_data()

    st.markdown("<h4>Analyses</h4>", unsafe_allow_html=True)
    st.markdown("<h6>Vehicle sold based on the cylinder distribution</h6>", unsafe_allow_html=True)
    
    # Display the Plotly figure for Cylinder Count
    st.plotly_chart(eda.get_cylinder())
    
    # Display the Plotly figure for Vehicle Type
    st.plotly_chart(eda.get_vehicle_type())

    # Display the Price Distribution
    st.plotly_chart(eda.get_price_dist())

    # Display the Top 5 Manufacturers based on popular cylinders
    st.plotly_chart(eda.get_top_5_manufacturers_cylinder())

    # Display sales by price range
    st.plotly_chart(eda.get_price_range_fig())

    # pie Chart showing unit sales sales by type
    st.plotly_chart(eda.get_top_5_vehicle_types_volume())

    # pie Chart showing sales revenue by type
    st.plotly_chart(eda.get_top_5_vehicle_types_revenue())

    

    st.markdown("<h4>Conclusion</h4>", unsafe_allow_html=True)
    st.markdown("""
        <ol>
            <li>The Top 5 selling Vehicles were: Ford, Chevrolet, Toyota, Honda, and Jeep.</li>
            <li>The Top selling vehicles based on their cylinders were 8, 6, 4, 5, and 10 in the same order.</li>
            <li>Most vehicles sold were equal to or less than $10,000.</li>
            <li>The charts show that the most frequently sold vehicles based on their types were: Trucks, SUVs, Sedan, Pickup, and Coupe in the same order which is consistent with top-selling vehicles, based on cylinders.</li>
            <li>We can also see that most sales of Trucks and SUVs are either with 8 or 6 cylinders, which means that customers prefer Ford and Chevrolet Trucks and SUVs with 8 cylinders as their first choice and 6 cylinders as their second choice.</li>
            <li>The variance between the sale of Truck, SUVs, and Sedan in units is only approximately 1%</li>
            <li>Although Trucks, SUV and sedans are the top 3 vehicles that are sold, the top 3 revenue earners are Trucks, SUVs, and Pickups, this means that the dealer should create marketing around these types of vehicles.</li>
        </ol>
        """, unsafe_allow_html=True)
    
else:
    st.write("Something went wrong. Contact Support")
