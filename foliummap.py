import folium
from folium.vector_layers import Circle
import pandas as pd
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication
from folium.features import Tooltip, Popup


#%%
# Read excel file
file_path = r"D:\baseline creation\NETWORK COORDINATES.xlsx"

# Assign excel file to panda dataframe
df = pd.read_excel(file_path)

# Load the data into a pandas dataframe
df = pd.read_csv('data.csv')

#%%
# Select all rows with True in the NGS CORS column
df_hubs = df.loc[df['NGS CORS'] == True]

# Select all rows with False in the NGS CORS column
df_other = df.loc[df['NGS CORS'] == False]

#%%
# Create a map centered on the mean of the locations in the dataframe
mean_lat = df['Lat dec'].mean()
mean_lon = df['Long dec'].mean()
map = folium.Map(location=[mean_lat, - mean_lon], zoom_start=12)

# Add a marker for each location in the dataframe
for index, row in df_hubs.iterrows():
    lat = row['Lat dec']
    lon = row['Long dec']
    site_code = row['Site Code']
    

    # Create the label content
    label = Tooltip(site_code)
    popup = Popup(site_code)  # Create the pop-up content

    #create marker
    marker = Circle(location=[lat, -lon], radius=5000, color='red', fill_color='red', tooltip=label,popup = popup)
    marker.add_to(map)



for index, row in df_other.iterrows():
    lat = row['Lat dec']
    lon = row['Long dec']
    site_code = row['Site Code']
    

    # Create the label content
    label = Tooltip(site_code)
    popup = Popup(site_code)  # Create the pop-up content

    #create marker
    marker = Circle(location=[lat, -lon], radius=5000, color='blue', fill_color='blue', tooltip=label,popup = popup)
    marker.add_to(map)


# Create the PySide6 application
app = QApplication()

# Create the QWebView widget and set its size
view = QWebEngineView()
# view.resize(400, 300)

# Load the map into the widget
view.setHtml(map._repr_html_())

# Show the widget
view.show()

# Run the PySide6 application
app.exec()