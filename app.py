import streamlit as st
import pandas as pd
import plotly_express as px

vehicle = pd.read_csv('vehicles_us.csv')
#Adding a new column to the dataframe with the result of an operation on existing columns for each car manufacturer
manu = []

for x in vehicle['model']:
    manu.append(x.split()[0])

vehicle['manufacturer'] = manu

#Fill NaN values with 0 to represent False (not available)
vehicle['is_4wd'] = vehicle['is_4wd'].fillna(0) 
#Fill NaN values with the mean of the model year since our data contains no significant outliers
#IQR = 7    Q1 = 2007   Q3 = 2014   OUTLIERS ABOVE 2025 AND BELOW 1996
vehicle['model_year'] = vehicle['model_year'].fillna(vehicle['model_year'].mean())
#Fill NaN values with the mean of the number of cylinders since our data contains no significant outliers
#IQR = 4    Q1 = 4   Q3 = 8   OUTLIERS ABOVE 14 AND BELOW -2
vehicle['cylinders'] = vehicle['cylinders'].fillna(vehicle['cylinders'].mean())
#Fill NaN values with the average milage since our data contains significant outliers
#IQR = 67360.0    Q1 = 79181.0   Q3 = 146541.0   OUTLIERS ABOVE 247581.0 AND BELOW -21859.0
vehicle['odometer'] = vehicle['odometer'].fillna(vehicle['odometer'].median())
#Fill color if not provided
vehicle['paint_color'] = vehicle['paint_color'].fillna('unknown')

#Change model_year to integer
vehicle['model_year'] = vehicle['model_year'].astype(int)
#Change cylinders to integer
vehicle['cylinders'] = vehicle['cylinders'].apply(lambda x : int(float(x)))
#Chaneg odometer to integer
vehicle['odometer'] = vehicle.odometer.round().astype(int)

#Adding a new column to the dataframe for a vehicles age based on the year this data was accessed (2019) from its model year
age = []

for y in vehicle['model_year']:
    age.append(2019 - y)
vehicle['age'] = age

#print(vehicle['model_year'].quantile(.75))
#print(vehicle['model_year'].quantile(.25))

#print(vehicle['cylinders'].quantile(.75))
#print(vehicle['cylinders'].quantile(.25))

#print(vehicle['odometer'].quantile(.75) + 1.5 * 67360.0)
#print(vehicle['odometer'].quantile(.25) - 1.5 * 67360.0)
st.header('Vehicle Data Explorer')
condition_options = sorted(vehicle['condition'].unique())
selected_cond = st.selectbox('Select vehicle condition:', 
                             condition_options, 
                             index = condition_options.index('excellent'))

st.dataframe(vehicle[vehicle['condition'] == selected_cond])

st.header('Histogram of all Vehicles with Ad\'s')
show_before_1990 = st.checkbox('Include vehicles made before 1990')
if not show_before_1990:
    vehicle = vehicle[vehicle['model_year'] >= 1990]
st.write(px.histogram(vehicle, x = 'manufacturer', color = 'model', nbins = 50, barmode = "overlay"))

#SCATTER PLOT FOR CAR AGE VS PRICE
st.header('Car Age vs Price')
st.write(px.scatter(vehicle, 
                             x = 'age', 
                             y = 'price', 
                             color = 'manufacturer', 
                             trendline =  "ols", 
                             trendline_scope = 'overall'))
#price_scat_plot = px.scatter(vehicle, x = 'age', y = 'price', color = 'manufacturer', trendline =  "ols", trendline_scope = 'overall')
#price_scat_plot.show()

#HISTOGRAM FOR ODOMETER VS VEHICLE CONDITION
st.header('Histogram for Odometer vs Condition:')
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None

st.write(px.histogram(vehicle, x = 'odometer', 
                      color = 'condition', 
                      nbins = 50, histnorm = 
                      histnorm, barmode = 'overlay'))
#odo_hist = px.histogram(vehicle, x = 'odometer', color = 'condition', nbins = 50, barmode = 'overlay')
#odo_hist.show()