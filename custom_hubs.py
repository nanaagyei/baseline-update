from IPython.display import display
from folium.features import Tooltip, Popup
from PySide6.QtWebEngineWidgets import QWebEngineView
from folium.vector_layers import Circle, PolyLine
from sklearn.cluster import KMeans
from xml.dom import minidom
import sqlite3
import numpy as np
import pandas as pd
import openpyxl
import folium
from geopy import distance
import geopy.distance
from sklearn.neighbors import NearestNeighbors
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostringlist
import fileloader
import sys
from PySide6.QtWidgets import QApplication
import pickle


# %%

def tuple_to_list(arr):
    my_list = [list(t) for t in arr]
    new_arr = np.array(my_list)
    return new_arr


def single_hub_df(main_df, sub_df):
    mask = main_df["Lat dec"].isin(
        sub_df["Lat dec"]) & main_df["Long dec"].isin(sub_df["Long dec"])
    df_region = main_df[mask]
    return df_region


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


def get_sorted_means(summary):
    means = dict(summary.mean())
    means = {k: v for k, v in sorted(means.items(), key=lambda item: item[1])}
    return means


def remove_selected_hub(site_code_dict, selected_single_hub):
    value_to_remove = selected_single_hub
    keys_to_remove = []

    for key, value in site_code_dict.items():
        if value == value_to_remove:
            keys_to_remove.append(key)

    for one_key in keys_to_remove:
        site_code_dict.pop(one_key)


def comp_cors_distances(df, column_name, index="Site Code"):
    df = df.reset_index(drop=True)
    true_df = df[df[column_name] == True].reset_index(drop=True)
    false_df = df[df[column_name] == True].reset_index(drop=True)
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


def calc_distance(point1, point2):
    return geopy.distance.distance(point1, point2, ellipsoid="GRS-80").km


def load_df():
    global df
    try:
        with open('df.pkl', 'rb') as f:
            df = pickle.load(f)
    except:
        pass

    return df

# Read excel file
# file_path = r"NETWORK COORDINATES.xlsx"



df = load_df()

cluster_df = df[['Site Code', 'Lat dec', 'Long dec']]
lo_la_df = df[['Lat dec', 'Long dec']]
X = np.array(lo_la_df.values.tolist())

# Get user input for number of clusters and hubs
n_clusters = int(input("Enter number of clusters: "))
n_hubs = int(input("Enter number of hubs: "))

kmeans = KMeans(n_clusters=n_clusters,
                n_init='auto', random_state=0).fit(X)
labels = kmeans.predict(X)

regions = list(range(n_clusters))
region_dict = {i: [] for i in regions}

for i in range(len(X)):
    region_dict[labels[i]].append(X[i])

clusters = [pd.DataFrame(region_dict[i], columns=[
    'Lat dec', 'Long dec']) for i in regions]

df_clusters = []
selected_hubs = []
site_code_dicts = []

for sub_df in clusters:
    single_df = single_hub_df(df, sub_df)
    df_clusters.append(single_df)
    dist_summary = comp_distances(single_df, "NGS CORS", "Site Code")
    means = get_sorted_means(dist_summary)
    selected_single_hub = list(means.keys())[0]
    selected_hubs.append(selected_single_hub)

# Extract hubs from each cluster
mask = df["Site Code"].isin(selected_hubs)
new_df = df[mask]

# Extract n_hubs of the least distance
distances = []

for i, row in new_df.iterrows():
    for j, other_row in new_df.iterrows():
        if i != j:
            point1 = (row["Lat dec"], row["Long dec"])
            point2 = (other_row["Lat dec"], other_row["Long dec"])
            distance = calc_distance(point1, point2)
            distances.append(
                (distance, row["Site Code"], other_row["Site Code"]))

distances.sort()

selected_distances = {}
count = 0

previous_start = None
previous_end = None
for distance, start, end in distances:
    if (start != end) and (start != previous_start or end != previous_end) and (start != previous_end or end != previous_start) and count < n_hubs:
        selected_distances[f"{start} to {end}"] = distance
        count += 1
        previous_start = start
        previous_end = end

hub_baselines_df = pd.DataFrame(columns=["start", "end"])

for key, value in selected_distances.items():
    start, end = key.split(" to ")
    df_temp = pd.DataFrame({"start": [start], "end": [end]})
    hub_baselines_df = pd.concat(
        [hub_baselines_df, df_temp], ignore_index=True)

# Create dictionaries to populate XML
site_code_dictionaries = []
for i in range(n_clusters):
    df_cluster = df_clusters[i]
    selected_hub = selected_hubs[i]
    code_df = df_cluster["Site Code"]
    code_dict = code_df.to_dict()

    value_to_remove = selected_hub
    keys_to_remove = []

    for key, value in code_dict.items():
        if value == value_to_remove:
            keys_to_remove.append(key)

    for one_key in keys_to_remove:
        code_dict.pop(one_key)

    site_code_dictionaries.append(code_dict)

# Create dictionary for hubs
true_df = df[df["NGS CORS"] == True]
cors_summary = true_df["Site Code"]
cors_dict = cors_summary.to_dict()

for value in selected_hubs:
    keys_to_remove = []
    for key, val in cors_dict.items():
        if val == value:
            keys_to_remove.append(key)

    for key in keys_to_remove:
        cors_dict.pop(key)


# print("_"*70 + "new CORS" + "_"*70)
# print(cors_dict)
# print(len(cors_dict.items()))
# print(selected_hubs)

# %%
# POPULATE OPUS PROJECT JOB INPUT FILE

# create root element

root = ET.Element('OPTIONS')

# create BASELINES element
baselines = ET.SubElement(root, 'BASELINES')

# iterate over the dictionaries and selected hubs simultaneously
for dictionary, hub in zip(site_code_dictionaries, selected_hubs):
    # iterate over the key-value pairs in the dictionary
    for key, value in dictionary.items():
        distance = ET.SubElement(baselines, 'DISTANCE')
        from_point = ET.SubElement(distance, 'FROM')
        from_point.text = hub
        to_point = ET.SubElement(distance, 'TO')
        to_point.text = value

# Iterate over the rows of the hub_baselines_df DataFrame
for i, row in hub_baselines_df.iterrows():
    # Extract the start and end point codes
    start = row["start"]
    end = row["end"]

    # Create a DISTANCE element
    distance = ET.SubElement(baselines, 'DISTANCE')
    # Create a FROM element and set its text to the value of the start point code
    from_point = ET.SubElement(distance, 'FROM')
    from_point.text = start
    # Create a TO element and set its text to the value of the end point code
    to_point = ET.SubElement(distance, 'TO')
    to_point.text = end

# create CORS element
# Shows cors that must be included
cors = ET.SubElement(root, 'CORS')
for value in selected_hubs:
    hub1 = ET.SubElement(cors, 'HUB')
    hub1.text = value
    fix1 = ET.SubElement(hub1, 'FIX')
    fix1.text = '3-D'

# CORS that are not hubs but must be included as well
for value in cors_dict.values():
    hub2 = ET.SubElement(cors, 'HUB')
    hub2.text = value
    fix2 = ET.SubElement(hub2, 'FIX')
    fix2.text = 'NONE'

# find all the DISTANCE elements in the BASELINES element
distances = baselines.findall('DISTANCE')

# print the number of DISTANCE elements
# print(len(distances))

# prettify the XML and print it
# xml_str = minidom.parseString(ET.tostring(root)).toprettyxml()
# print(xml_str)
# ___________________________________________________________
# create XML tree
tree = ET.ElementTree(root)

# write pretty-printed XML tree to file
xml_str = ET.tostring(root)
dom = minidom.parseString(xml_str)
with open('options.xml', 'w') as f:
    dom.writexml(f, indent='  ', addindent='  ',
                    newl='\n', encoding='utf-8')

# # print pretty-printed XML tree to console
# with open('options.xml', 'r') as f:
#     print(f.read())

# %%
# map display dataframes
# helps create baselines



filtered_map_dfs = []
# extract site codes dataframes,to use to construct polylines(the "TO" stations)
for site_code_dict in site_code_dictionaries:
    map_baseline_df = pd.DataFrame.from_dict(
        site_code_dict, orient='index', columns=['Site Code'])
    # print(map_baseline_df)
    map_mask = df['Site Code'].isin(map_baseline_df['Site Code'])
    filtered_map_df = df[map_mask]
    filtered_map_dfs.append(filtered_map_df)
    # print(filtered_map_df)

# print(filtered_map_dfs[0])

# print(selected_hubs)
map_hub_mask = df['Site Code'].isin(selected_hubs)
filtered_s_hub_map_df = df[map_hub_mask]
sorting_index = np.argsort(np.array(selected_hubs))
filtered_s_hub_map_df = filtered_s_hub_map_df.iloc[sorting_index]
# print(filtered_s_hub_map_df)

# display start and end coordinates for the hub connections
# split the 4 shortest hub selected distance dataframes into to, one for start
hub_connection_start_df = hub_baselines_df[['start']]
hub_connection_start_resulting_df = pd.DataFrame(columns=df.columns)
for value in hub_connection_start_df['start']:
    temp_df = df.loc[df['Site Code'] == value]
    hub_connection_start_resulting_df = pd.concat(
        [hub_connection_start_resulting_df, temp_df], ignore_index=True)

# split the 4 shortest hub selected distance dataframes into to, one for end
hub_connection_end_df = hub_baselines_df[['end']]
hub_connection_end_resulting_df = pd.DataFrame(columns=df.columns)
for value in hub_connection_end_df['end']:
    temp_df = df.loc[df['Site Code'] == value]
    hub_connection_end_resulting_df = pd.concat(
        [hub_connection_end_resulting_df, temp_df], ignore_index=True)


# print(hub_baselines_df)
# print(hub_connection_start_df)
# print(hub_connection_start_resulting_df)

# print(hub_connection_end_df)
# print(hub_connection_end_resulting_df)


# %%


def create_default_map():
    # Create a map centered on the USA
    map = folium.Map(location=[38.0, -97.0], zoom_start=5)

    # Return the map
    return map


def create_map(site_code_dictionaries, hub_baselines_df, df_clusters):
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

    # Add polylines for each cluster
    for j in range(len(site_code_dictionaries)):
        sub_df = df_clusters[j]
        end_coords = [df.loc[df['Site Code'] == list(site_code_dictionaries[j].keys())[0]]['Lat dec'].values[0], -1 * abs(
            df.loc[df['Site Code'] == list(site_code_dictionaries[j].keys())[0]]['Long dec'].values[0])]
        for i, row in sub_df.iterrows():
            start_coords = [row['Lat dec'], -row['Long dec']]
            line = folium.PolyLine(
                locations=[start_coords, end_coords], color='blue', weight=2, opacity=1)
            line.add_to(polyline_layer)
            polyline_layer.add_to(map)

    # Add polylines for the shortest hub connections
    for i, row in hub_baselines_df.iterrows():
        # Get the coordinates of the start marker
        start_coords = [row["start"]["Lat dec"], -row["start"]["Long dec"]]
        # Get the coordinates of the end marker
        end_coords = [row["end"]["Lat dec"], -row["end"]["Long dec"]]
        # Create the PolyLine object
        line = folium.PolyLine(
            locations=[start_coords, end_coords], color='blue', weight=2, opacity=1)
        # Add the line to the polyline layer
        polyline_layer.add_child(line)
        # Add the polyline layer to the map
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
    map.save('map1.html')
    return map

map = create_map(site_code_dictionaries, hub_baselines_df, df_clusters)
# print("Number of receivers: ", df.shape[0])
# print("Number of independent baselines: ", len(distances))

# %%

# all functions:

# def tuple_to_list(arr):
#     my_list = [list(t) for t in arr]
#     new_arr = np.array(my_list)
#     return new_arr

# # slicing the df into a dataframe for each cluster


# def single_hub_df(main_df, sub_df):
#     mask = main_df["Lat dec"].isin(
#         sub_df["Lat dec"]) & main_df["Long dec"].isin(sub_df["Long dec"])
#     df_region = main_df[mask]
#     return df_region

# # function to compute distances


# def comp_distances(df, column_name, index="Site Code"):
#     df = df.reset_index(drop=True)
#     true_df = df[df[column_name] == True].reset_index(drop=True)
#     false_df = df[df[column_name] == False].reset_index(drop=True)
#     dist = []
#     true_dist = pd.DataFrame()
#     for i in range(len(true_df[index])):
#         for j in range(len(false_df[index])):
#             trues = (true_df["Lat dec"][i], true_df["Long dec"][i])
#             falses = (false_df["Lat dec"][j], false_df["Long dec"][j])
#             dist.append(distance.distance(
#                 trues, falses, ellipsoid="GRS-80").km)
#         true_dist[true_df[index][i]] = dist
#         dist = []
#     return true_dist.set_index(false_df[index])

# # Sort the means


# def get_sorted_means(summary):
#     means = dict(summary.mean())
#     means = {k: v for k, v in sorted(means.items(), key=lambda item: item[1])}
#     return means


# def remove_selected_hub(site_code_dict, selected_single_hub):
#     value_to_remove = selected_single_hub
#     keys_to_remove = []

#     for key, value in site_code_dict.items():
#         if value == value_to_remove:
#             keys_to_remove.append(key)

#     for one_key in keys_to_remove:
#         site_code_dict.pop(one_key)


# def comp_cors_distances(df, column_name, index="Site Code"):
#     df = df.reset_index(drop=True)
#     true_df = df[df[column_name] == True].reset_index(drop=True)
#     false_df = df[df[column_name] == True].reset_index(drop=True)
#     dist = []
#     true_dist = pd.DataFrame()
#     for i in range(len(true_df[index])):
#         for j in range(len(false_df[index])):
#             trues = (true_df["Lat dec"][i], true_df["Long dec"][i])
#             falses = (false_df["Lat dec"][j], false_df["Long dec"][j])
#             dist.append(distance.distance(
#                 trues, falses, ellipsoid="GRS-80").km)
#         true_dist[true_df[index][i]] = dist
#         dist = []
#     return true_dist.set_index(false_df[index])

# # %%
# # Define a function to calculate the distance between two points


# def calc_distance(point1, point2):
#     return geopy.distance.distance(point1, point2, ellipsoid="GRS-80").km


# # %%

# # Load the df variable from the file
# def load_df():
#     global df
#     try:
#         with open('df.pkl', 'rb') as f:
#             df = pickle.load(f)
#     except:
#         pass

#     return df


# # Read excel file
# # file_path = r"D:\baseline creation\NETWORK COORDINATES.xlsx"
# file_path = r"SC NETWORK COORDINATES.xlsx"

# # Assign excel file to panda dataframe
# df = pd.read_excel(file_path)
# # print(df)

# # ectract long and lat from xcel file
# cluster_df = df[['Site Code', 'Lat dec', 'Long dec']]
# lo_la_df = df[['Lat dec', 'Long dec']]
# # print(cluster_df)

# # print(len(cluster_df))
# # convert into list
# lo_la_list = lo_la_df.values.tolist()
# # print(lo_la_list)83

# # %%
# # CUSTOM CLUSTERING
# # Clustering
# X = np.array(lo_la_list)
# # Prompt user for number of clusters
# num_clusters = input("Enter the number of clusters: ")

# # Convert user input to integer
# num_clusters = int(num_clusters)

# # Generate empty lists to store clusters
# clusters = []
# for i in range(num_clusters):
#     clusters.append([])

# # Perform clustering and store clusters in lists
# kmeans = KMeans(n_clusters=num_clusters, n_init='auto', random_state=0).fit(X)
# labels = kmeans.predict(X)

# for i in range(len(X)):
#     clusters[labels[i]].append(X[i])

# # Create dataframes for each cluster
# df_clusters = []
# selected_hubs = []
# site_code_dicts = []


# FOR SINGLE HUB

# for i in range(num_clusters):
#     # Create dataframe for current cluster
#     cluster_df = pd.DataFrame(clusters[i], columns=['Lat dec', 'Long dec'])
#     cluster_df["Site Code"] = df["Site Code"]

#     # Compute distances and select hub site code for current cluster
#     single_df = single_hub_df(df, cluster_df)
#     df_clusters.append(single_df)
#     dist_summary = comp_distances(single_df,"NGS CORS","Site Code")
#     print("Distance Summary: ")
#     print(dist_summary)
#     print("="*70)
#     means = get_sorted_means(dist_summary)
#     print("Means: ")
#     print(means)
#     print("="*70)
#     selected_single_hub = list(means.keys())[0]
#     selected_hubs.append(selected_single_hub)

# print(selected_hubs)

# FOR CUSTOM HUB
# Prompt user for number of single hub sites to select
# num_hubs = input("Enter the number of single hub sites to select: ")

# # Convert user input to integer
# num_hubs = int(num_hubs)

# for i in range(num_clusters):
#     # Create dataframe for current cluster
#     cluster_df = pd.DataFrame(clusters[i], columns=['Lat dec', 'Long dec'])
#     cluster_df["Site Code"] = df["Site Code"]

#     # Compute distances and select hub site code for current cluster
#     single_df = single_hub_df(df, cluster_df)
#     df_clusters.append(single_df)
#     dist_summary = comp_distances(single_df, "NGS CORS", "Site Code")
#     # print("Distance Summary: ")
#     # print(dist_summary)
#     # print("="*70)
#     # Select the top num_single_hubs sites according to mean distance
#     means = get_sorted_means(dist_summary)
#     print("Means: ")
#     print(means)
#     print("="*70)
#     # If user input exceeds the number of sites in the cluster, print "yawa"
#     if num_hubs > len(means):
#         print("yawa")
#     else:
#         custom_hubs = list(means.keys())[:num_hubs]
#         selected_hubs.extend(custom_hubs)

# print(selected_hubs)

# for all hubs
# for i in range(num_clusters):
#     # Create dataframe for current cluster
#     cluster_df = pd.DataFrame(clusters[i], columns=['Lat dec', 'Long dec'])
#     cluster_df["Site Code"] = df["Site Code"]

#     # Compute distances and select hub site code for current cluster
#     single_df = single_hub_df(df, cluster_df)
#     df_clusters.append(single_df)
#     dist_summary = comp_distances(single_df,"NGS CORS","Site Code")
#     print("Distance Summary: ")
#     print(dist_summary)
#     print("="*70)
#     means = get_sorted_means(dist_summary)
#     print("Means: ")
#     print(means)
#     print("="*70)
#     all_hubs = list(means.keys())
#     selected_hubs.append(all_hubs)

# print(selected_hubs)

# Extract rows corresponding to selected hub site codes
# mask = df["Site Code"].isin(selected_hubs)
# new_df = df[mask]
# print(new_df)

# %%
