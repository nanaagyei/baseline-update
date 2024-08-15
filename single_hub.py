from IPython.display import display
from folium.features import Tooltip, Popup
from PySide6.QtWebEngineWidgets import QWebEngineView
from folium.vector_layers import Circle, PolyLine
import folium
from xml.dom import minidom
import sqlite3
import pandas as pd
import numpy as np
import openpyxl
from geopy import distance
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostringlist
import fileloader
import sys
from PySide6.QtWidgets import QApplication
import pickle


# %%
# function to compute distances
def comp_distances(df, column_name, index="Site Code"):
    df = df.reset_index(drop=True)
    true_df = df[df[column_name] == True].reset_index(drop=True)
    false_df = df[df[column_name] == False].reset_index(drop=True)
    dist = []
    true_dist = pd.DataFrame()
    for i in range(len(true_df[index])):
        for j in range(len(false_df[index])):
            trues = (true_df["Lat dec"][i], true_df["Long dec"][i])
            falses = (false_df["Lat dec"][j], false_df["Long dec"][j])
            dist.append(distance.distance(
                trues, falses, ellipsoid="GRS-80").km)
        true_dist[true_df[index][i]] = dist
        dist = []
    return true_dist.set_index(false_df[index])

# Sort the means


def get_sorted_means(summary):
    means = dict(summary.mean())
    means = {k: v for k, v in sorted(means.items(), key=lambda item: item[1])}
    return means

# remove selected hub from dictionary


def remove_hub(value, dict_hub):
    keys_to_remove = []

    for key, val in dict_hub.items():
        if val == value:
            keys_to_remove.append(key)

    for one_key in keys_to_remove:
        dict_hub.pop(one_key)
    return

# read file using file path
# def read_file(file_path):
#     df = pd.read_excel(file_path)
#     return df
# %%
# Read the CSV file into a pandas DataFrame
# app = QApplication(sys.argv)
# win = MainWindow()
# df = df.get_data()


# Load the df variable from the file
def load_df():
    global df
    try:
        with open('df.pkl', 'rb') as f:
            df = pickle.load(f)
    except:
        pass

    return df

# print(df)
# win.show()


# Read excel file
# file_path = r"D:\baseline creation\NETWORK COORDINATES.xlsx"

# # Assign excel file to panda dataframe
# df = pd.read_excel(file_path)


# df = read_file(file_path)
# %%
# HUB SELECTION

def hub_selection():
    df = load_df()
    # Output the summary of the distances
    dist_summary = comp_distances(df, "NGS CORS", "Site Code")
    # print(dist_summary)

    # Output the sorted average of the distances in ascending order(smallest to largest)
    means = get_sorted_means(dist_summary)
    # print("_"*70 + "Average distances" + "_"*70)
    # print(means)

    # Extract the least of the averaged distance into a variable called selected_single_hub
    selected_single_hub = list(means.keys())[0]
    # print("Suggested Hub is:",selected_single_hub)
    # print(type(selected_single_hub))

    # %%
    #
    # ##Create a dictionaries to populate xml

    # 1 extract site code coulmn from pandas dataframe
    site_code_df = df["Site Code"]
    # print(site_code_df)
    site_code_dict = dict(site_code_df)
    # print(site_code_dict)

    # remove the selected hub from the dictionary
    remove_hub(selected_single_hub, site_code_dict)

    # value_to_remove = selected_single_hub
    # keys_to_remove = []

    # for key, value in site_code_dict.items():
    #     if value == value_to_remove:
    #         keys_to_remove.append(key)

    # for one_key in keys_to_remove:
    #     site_code_dict.pop(one_key)

    # print("_"*70 + "new dict" + "_"*70)
    # print(site_code_dict)

    # 2 extract CORS from pandas dataframe
    true_df = df[df["NGS CORS"] == True]
    # print(true_df)
    for i in range(len(true_df)):
        cors_summary = true_df["Site Code"]
    # print(cors_summary)
    # print("_"*70 + "old CORS" + "_"*70)
    cors_dict = cors_summary.to_dict()

    # print(cors_dict)

    # remove the selected hub from the dictionary
    # value_to_remove = selected_single_hub
    # keys_to_remove = []

    # for key, value in cors_dict.items():
    #     if value == value_to_remove:
    #         keys_to_remove.append(key)

    # for one_key in keys_to_remove:
    #     cors_dict.pop(one_key)

    remove_hub(selected_single_hub, cors_dict)
    # print("_"*70 + "new CORS" + "_"*70)
    # print(cors_dict)
    return (selected_single_hub, site_code_dict, cors_dict)

# %%


def get_database_data(database_file):
    # Connect to the database
    conn = sqlite3.connect(database_file)

    # Read the combo_box_values table from the database into a dataframe
    df = pd.read_sql_query("SELECT * FROM combo_box_values", conn)

    return df


# Get the data from the on_combo_box_database.db database
def get_data():
    constraint_weight_df = get_database_data("on_combo_box_database.db")
    # print(constraint_weight_df)

    # Get the data from the geoid_combo_box_database.db database
    geoid_df = get_database_data("geoid_combo_box_database.db")
    return constraint_weight_df, geoid_df
# print(geoid_df)


# %%
# POPULATE OPUS PROJECT JOB INPUT FILE

def populate_xml_file(file_name, constraint_weight_text, element_cutoff_text, email, geoid_model_text, reference_frame_text, gnss_text, tropo_interval_text, tropo_model_text):
    selected_single_hub, site_code_dict, cors_dict = hub_selection()
    constraint_weight_df, geoid_df = get_data()

    # create root element
    root = ET.Element('OPTIONS')

    # create BASELINES element
    baselines = ET.SubElement(root, 'BASELINES')

    for key, value in site_code_dict.items():
        distance = ET.SubElement(baselines, 'DISTANCE')
        from_point = ET.SubElement(distance, 'FROM')
        from_point.text = selected_single_hub
        to_point = ET.SubElement(distance, 'TO')

        to_point.text = value

    # create CONSTRAINT_WEIGHT element
    # Iterate over the rows of the constraint_weight_df dataframe
    for index, row in constraint_weight_df.iterrows():
        # Get the string_value from the row
        string_value = row['string_value']

    constraint_weight = ET.SubElement(root, 'CONSTRAINT_WEIGHT')

    # Set the text of the subelement to the string from the dataframe
    constraint_weight.text = constraint_weight_text

    # create ELEVATION_CUTOFF element
    elevation_cutoff = ET.SubElement(root, 'ELEVATION_CUTOFF')
    elevation_cutoff.text = element_cutoff_text

    # create EMAIL_ADDRESS element
    email_address = ET.SubElement(root, 'EMAIL_ADDRESS')
    email_address.text = email

    # create GEOID_MODEL element
    geoid_model = ET.SubElement(root, 'GEOID_MODEL')
    geoid_model.text = geoid_model_text

    # create REFERENCE_FRAME element
    reference_frame = ET.SubElement(root, 'REFERENCE_FRAME')
    reference_frame.text = reference_frame_text

    # create GNSS element
    gnss = ET.SubElement(root, 'GNSS')
    gnss.text = gnss_text

    # create TROPO_INTERVAL element
    tropo_interval = ET.SubElement(root, 'TROPO_INTERVAL')
    tropo_interval.text = tropo_interval_text

    # create TROPO_MODEL element
    tropo_model = ET.SubElement(root, 'TROPO_MODEL')
    tropo_model.text = tropo_model_text

    # ________________________________________________________
    # create CORS element
    # Shows cors that must be included
    cors = ET.SubElement(root, 'CORS')

    # CORS that is  HUB element
    hub1 = ET.SubElement(cors, 'HUB')
    hub1.text = selected_single_hub
    fix1 = ET.SubElement(hub1, 'FIX')
    fix1.text = '3-D'

    # CORS that are not hubs but must be included as well
    for key, value in cors_dict.items():
        hub2 = ET.SubElement(cors, 'HUB')
        hub2.text = value
        fix2 = ET.SubElement(hub2, 'FIX')
        fix2.text = 'NONE'

    # ___________________________________________________________-

    # find all the DISTANCE elements in the BASELINES element
    distances = baselines.findall('DISTANCE')

    # print the number of DISTANCE elements
    # print(len(distances))

    # create XML tree
    tree = ET.ElementTree(root)

    # write pretty-printed XML tree to file
    xml_str = ET.tostring(root)
    dom = minidom.parseString(xml_str)
    with open(str(file_name), 'w') as f:
        dom.writexml(f, indent='  ', addindent='  ',
                     newl='\n', encoding='utf-8')

# # ##print pretty-printed XML tree to console
# with open('testoptions.xml', 'r') as f:
#     print(f.read())


# %%
# map display dataframes
# helps create baselines
# print(site_code_dict)
def display_dataframe():
    selected_single_hub, site_code_dict, cors_dict = hub_selection()
    map_baseline_df = pd.DataFrame.from_dict(
        site_code_dict, orient='index', columns=['Site Code'])
    # print(df)
    # print(map_baseline_df)

    map_mask = df['Site Code'].isin(map_baseline_df['Site Code'])
    filtered_map_df = df[map_mask]
    # print(filtered_map_df)

    # print(selected_single_hub)
    s_hub_map_df = pd.DataFrame({'Site Code': selected_single_hub}, index=[0])
    # print(s_hub_map_df)

    map_hub_mask = df['Site Code'].isin(s_hub_map_df['Site Code'])
    filtered_s_hub_map_df = df[map_hub_mask]

    return filtered_map_df, filtered_s_hub_map_df
# print(filtered_s_hub_map_df)

# %%
# map display


def create_default_map():
    # Create a map centered on the mean of the locations in the dataframe
    # mean_lat = df['Lat dec'].mean()
    # mean_lon = df['Long dec'].mean()
    # map = folium.Map(location=[mean_lat, - mean_lon], zoom_start=6.5)

    # Create a map centered on the USA
    map = folium.Map(location=[38.0, -97.0], zoom_start=5)

    # Return the map
    return map

# %%


def create_single_hub_map():
    filtered_map_df, filtered_s_hub_map_df = display_dataframe()
    # Select all rows with True in the NGS CORS column
    df_hubs = df.loc[df['NGS CORS'] == True]

    # Select all rows with False in the NGS CORS column
    df_other = df.loc[df['NGS CORS'] == False]

    # %%
    # Create a map centered on the mean of the locations in the dataframe
    mean_lat = df['Lat dec'].mean()
    mean_lon = df['Long dec'].mean()
    map = folium.Map(location=[mean_lat, - mean_lon], zoom_start=6.5)

    # Create a FeatureGroup for the polylines
    polyline_layer = folium.FeatureGroup(name='Baselines')

    # Create a FeatureGroup for the first markers
    ngs_cors_marker_layer = folium.FeatureGroup(name='NGS CORS')

    # Create a FeatureGroup for the second markers
    stations_marker_layer = folium.FeatureGroup(name='Stations')

    # Add the FeatureGroups to the map
    polyline_layer.add_to(map)
    ngs_cors_marker_layer.add_to(map)
    stations_marker_layer.add_to(map)

    # Add a marker for each location in the dataframe
    for index, row in df_hubs.iterrows():
        lat = row['Lat dec']
        lon = row['Long dec']
        site_code = row['Site Code']

        # Create the label content
        label = Tooltip(site_code)
        popup = Popup(site_code)  # Create the pop-up content

        # create marker
        marker = Circle(location=[lat, -lon], radius=5000, color='red',
                        fill_color='red', fill_opacity=1, tooltip=label, popup=popup)
        marker.add_to(ngs_cors_marker_layer)
        ngs_cors_marker_layer.add_to(map)

    for index, row in df_other.iterrows():
        lat = row['Lat dec']
        lon = row['Long dec']
        site_code = row['Site Code']

        # Create the label content
        label = Tooltip(site_code)
        popup = Popup(site_code)  # Create the pop-up content

        # create marker
        marker = Circle(location=[lat, -lon], radius=5000, color='blue',
                        fill_color='blue', fill_opacity=1, tooltip=label, popup=popup)
        marker.add_to(stations_marker_layer)
        stations_marker_layer.add_to(map)

    # Get the end_coords from df5
    end_coords = [filtered_s_hub_map_df['Lat dec'], -
                  1 * abs(filtered_s_hub_map_df['Long dec'])]

    # Iterate over the rows of filtered_df
    for i, row in filtered_map_df.iterrows():
        # Get the coordinates of the start marker
        start_coords = [row['Lat dec'], -row['Long dec']]

        # Create the PolyLine object
        line = folium.PolyLine(
            locations=[start_coords, end_coords], color='blue', weight=2, opacity=1)

        line.add_to(polyline_layer)
        # Add the line to the map
        polyline_layer.add_to(map)

    # Create a Stamen Toner tileset
    stamen_toner = folium.TileLayer(
        tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.png',
        attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.',
        name='Stamen Toner',
        max_zoom=18,
        min_zoom=0,
        show=True
    )

    # Add the tileset to the map
    stamen_toner.add_to(map)

    # Add the layer control to the map
    folium.LayerControl().add_to(map)

    # Add the Stamen Toner tileset to the map
    stamen_toner.add_to(map)

    # Save the map to an HTML file
    map.save('map.html')

    return map


# print("Number of receivers: ", df.shape[0])
# print("Number of independent baselines: ", len(distances))
