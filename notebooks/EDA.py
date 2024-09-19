#!/usr/bin/env python
# coding: utf-8

# In[1]:


# EDA.py


# ## Import Libraries

# In[2]:


import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import scipy.stats as stats
import numpy as np
import plotly.express as px
from scipy.stats import gaussian_kde


# ## Initializing global variables. They are made global to allow access to multiple functions.

# In[3]:


# Global variables
csv_path = None
df = None
df_loaded = "File not found"
cylinder_fig = None
vehicle_type_fig = None
price_dist_fig = None
top_5_manufacturers_cylinder_fig = None
price_range_fig = None
top_5_vehicle_types_volume_fig = None
top_5_vehicle_types_revenue_fig = None


# ## Loading the data. This code ensures that the data file is accessed via its relative path

# In[4]:


def load_data():
    global df
    global csv_path
    global df_loaded

    if df is None:  # Only load if df hasn't been loaded already
        # CSV filename
        csv_filename = 'vehicles_us.csv'

        # Construct the relative path to the CSV file
        script_dir = os.path.dirname(__file__)
        csv_path = os.path.join(script_dir, '..', csv_filename)  # Adjust as needed

        # Print for debugging
        print(f"Constructed CSV path: {csv_path}")

        # Check if the file exists
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df_loaded = "Data loaded successfully"
        else:
            df_loaded = "File not found"
    return df_loaded



# ## Cleaning data

# In[5]:


def cleanup_data():
    global df
    # check for duplicates 
    duplicate_rows = df[df.duplicated()]
    num_duplicates = df.duplicated().sum()
    #print(f"Number of duplicate rows: {num_duplicates}")
    print("Duplicates found:",num_duplicates)

    if num_duplicates > 0:
        # Remove duplicates
        df = df.drop_duplicates()

    # Replace NaN with False and non-NaN with True in the 'is_4wd' column
    df['is_4wd'] = df['is_4wd'].notna()
    
    # Several empty cells exist. Filling This fills missing values in the 'cylinders','odometer' and 'model_year' column with the 
    # corresponding median 'cylinders','odometer' and 'model_year' value within each group of the 'type' column.
    
    df['cylinders'] = df[['cylinders', 'type']].groupby('type').transform(lambda x:x.fillna(x.median()))
    df['odometer'] = df[['odometer', 'type']].groupby('type').transform(lambda x:x.fillna(x.median()))
    df['model_year'] = df[['model_year', 'type']].groupby('type').transform(lambda x:x.fillna(x.median()))

    # Remove all rows with any NaN values
    df = df.dropna()

    # List of columns to capitalize the first letter of each word
    columns_to_capitalize = ['model', 'condition', 'fuel', 'transmission', 'type', 'paint_color']

    # Capitalize the first letter of each word in the specified columns using .loc[]
    for column in columns_to_capitalize:
        df.loc[:, column] = df[column].str.title()

    # Remove rows where price > 100000 or price < 300
    df = df[(df['price'] <= 100000) & (df['price'] >= 300)]

    #Adding column for manufaturer as this will be used in subsequent analyses
    df.loc[:, 'manufacturer'] = df['model'].apply(lambda x: x.split()[0])
    
    
    return


# ## Data Analysis and charting functions

# In[6]:


def analyze_data():
    global cylinder_fig
    global vehicle_type_fig
    global price_dist_fig
    global top_5_manufacturers_cylinder_fig
    global price_range_fig
    global top_5_vehicle_types_volume_fig
    global top_5_vehicle_types_revenue_fig

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Sales by cylinder count >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    # Create a DataFrame for Plotly
    df_cylinders = df['cylinders'].value_counts().reset_index()
    df_cylinders.columns = ['Cylinders Type', 'Frequency']  # Rename columns for clarity
    
    # Create a Plotly bar plot
    fig = px.bar(df_cylinders,
                 x='Cylinders Type', y='Frequency',
                 title='Cylinders Type Distribution',
                 labels={'Cylinders Type': 'Cylinders Type', 'Frequency': 'Frequency'})
    
    # Assign to Plotly chart variable
    cylinder_fig = fig


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Total Sales by vehicle type >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    # Show the chart
    #fig.show()

    # Group by type and calculate total sales
    total_sales_by_type = df.groupby('type')['price'].sum()
    
    # Create the bar chart
    fig = px.bar(total_sales_by_type, x=total_sales_by_type.index, y='price',
                title='Total Sales by Vehicle Type',
                labels={'x': 'Vehicle Type', 'y': 'Total Sales'})

    
    # Assign to Plotly chart variable
    vehicle_type_fig = fig




    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Price Distribution Curve >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    # Create the price distribution plot
    fig = px.histogram(
        df,
        x="price",
        nbins=10,  # Adjust the number of bins as needed
        histfunc="count",  # Use 'count' for the histogram
        marginal="rug",  # Add a rug plot along the x-axis
        title="Price Distribution Curve",
        labels={"price": "Price", "value": "Frequency"},
    )
    
    # Assign to Plotly chart variable
    price_dist_fig = fig




    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Top 5 Manufacturers based on most popular cylinders >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    # Filter data for cylinders 4, 6, and 8
    filtered_df = df[df['cylinders'].isin([4.0, 6.0, 8.0])]
    
    # Group by manufacturer and cylinder, and count occurrences
    cylinder_counts = filtered_df.groupby(['manufacturer', 'cylinders']).size().unstack(fill_value=0)
    
    # Sum counts for each manufacturer to get total count for sorting
    cylinder_counts['Total'] = cylinder_counts.sum(axis=1)
    
    # Get the top 5 manufacturers based on total count
    top_5_manufacturers = cylinder_counts['Total'].nlargest(5).index
    
    # Filter data for top 5 manufacturers
    top_5_df = cylinder_counts.loc[top_5_manufacturers]
    
    # Convert the DataFrame to long format for Plotly
    top_5_df_long = top_5_df.drop(columns='Total').reset_index().melt(id_vars='manufacturer', var_name='cylinders', value_name='count')
    
    # Plot with Plotly Express
    top_5_manufacturers_cylinder_fig = px.bar(top_5_df_long, 
                                             x='manufacturer', 
                                             y='count', 
                                             color='cylinders', 
                                             title='Top 5 Manufacturers by Cylinder Type',
                                             labels={'count': 'Number of Vehicles', 'manufacturer': 'Manufacturer', 'cylinders': 'Cylinders'},
                                             text='count',
                                             color_discrete_sequence=px.colors.qualitative.Plotly,
                                             category_orders={'cylinders': ['4.0', '6.0', '8.0']}
                                            )
    
    top_5_manufacturers_cylinder_fig.update_layout(barmode='stack', 
                                                   xaxis_title='Manufacturer',
                                                   yaxis_title='Number of Vehicles',
                                                   xaxis_tickangle=-45)


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Top 5 Manufacturers based on most popular cylinders >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # number of cars sold by price ranges
    # Define the price bins and labels
    price_bins = [0, 10000, 20000, 30000, 40000, 50000, 60000]
    price_labels = ['0-10000', '10001-20000', '20001-30000', '30001-40000', '40001-50000', '50001-60000']
    
    # Create a new column 'price_range' based on the bins
    df['price_range'] = pd.cut(df['price'], bins=price_bins, labels=price_labels)
    
    # Count the number of cars sold in each price range
    price_range_counts = df['price_range'].value_counts().sort_index()
    
    # Convert the result to a DataFrame for Plotly
    price_range_df = price_range_counts.reset_index()
    price_range_df.columns = ['Price Range', 'Number of Cars Sold']
    
    # Create a bar plot using Plotly
    price_range_fig = px.bar(price_range_df, 
                 x='Price Range', 
                 y='Number of Cars Sold', 
                 title='Number of Cars Sold by Price Range',
                 labels={'Price Range': 'Price Range', 'Number of Cars Sold': 'Number of Cars Sold'},
                 text='Number of Cars Sold',  # Display the number on the bars
                 color_discrete_sequence=['skyblue'])  # Color for bars
    
    # Update layout to rotate x-axis labels and adjust size
    price_range_fig.update_layout(xaxis_tickangle=-45, width=800, height=600)

    

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Top 5 Vehicle types sold (volume) >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    # Group by vehicle type and count the number of vehicles sold
    vehicle_type_counts = df['type'].value_counts().nlargest(5)

    # Create a DataFrame from the value counts
    vehicle_type_df = vehicle_type_counts.reset_index()
    vehicle_type_df.columns = ['Vehicle Type', 'Number of Vehicles Sold']

    # Create the pie chart using Plotly
    top_5_vehicle_types_volume_fig = px.pie(vehicle_type_df, 
                 names='Vehicle Type', 
                 values='Number of Vehicles Sold', 
                 title='Top 5 Vehicle Types Sold',
                 color_discrete_sequence=px.colors.qualitative.Set3)

    

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Top 5 Vehicle types sold (revenue) >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    

    # Group by vehicle type and calculate the total sales revenue
    revenue_by_vehicle_type = df.groupby('type')['price'].sum().nlargest(5)

    # Create a DataFrame from the grouped data
    vehicle_type_revenue_df = revenue_by_vehicle_type.reset_index()
    vehicle_type_revenue_df.columns = ['Vehicle Type', 'Total Sales Revenue']

    # Create the pie chart using Plotly
    top_5_vehicle_types_revenue_fig = px.pie(vehicle_type_revenue_df, 
                 names='Vehicle Type', 
                 values='Total Sales Revenue', 
                 title='Top 5 Vehicle Types by Sales Revenue',
                 color_discrete_sequence=px.colors.qualitative.Set3)


    return


# ## Public functions

# These functions are used by the frontend application (app.py) to access and display the charts, tables and calculations.

# In[7]:


def get_file_path():
    global csv_path
    return csv_path


# In[8]:


def get_df():
    global df
    global df_loaded
    if df is None:
        load_data()  # Load the data if not already loaded
    return


# In[9]:


def get_df_head():
    global df
    return df.head(5)


# In[10]:


def get_df_loaded_message():
    global df_loaded
    return df_loaded


# In[11]:


def get_cylinder():
    global cylinder_fig
    return cylinder_fig


# In[12]:


def get_vehicle_type():
    global vehicle_type_fig
    return vehicle_type_fig


# In[13]:


def get_price_dist():
    global price_dist_fig
    return price_dist_fig


# In[14]:


def get_top_5_manufacturers_cylinder():
    global top_5_manufacturers_cylinder_fig
    return top_5_manufacturers_cylinder_fig


# In[15]:


def get_price_range_fig():
    global price_range_fig
    return price_range_fig


# In[16]:


def get_top_5_vehicle_types_volume():
    global top_5_vehicle_types_volume_fig
    return top_5_vehicle_types_volume_fig


# In[17]:


def get_top_5_vehicle_types_revenue():
    global top_5_vehicle_types_revenue_fig
    return top_5_vehicle_types_revenue_fig

