from IPython.display import display
from folium.features import Tooltip, Popup
from PySide6.QtWebEngineWidgets import QWebEngineView
from folium.vector_layers import Circle, PolyLine
from xml.dom import minidom
import xml.etree.ElementTree as ET
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import folium
from geopy import distance
import geopy.distance
from sklearn.neighbors import NearestNeighbors
import fileloader
import sys
from PySide6.QtWidgets import QApplication
import pickle


# %%

# all functions:

def tuple_to_list(arr):
    my_list = [list(t) for t in arr]
    new_arr = np.array(my_list)
    return new_arr

# slicing the df into a dataframe for each cluster


def single_hub_df(main_df, sub_df):
    mask = main_df["Lat dec"].isin(
        sub_df["Lat dec"]) & main_df["Long dec"].isin(sub_df["Long dec"])
    df_region = main_df[mask]
    return df_region

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


# %%
# Define a function to calculate the distance between two points
def calc_distance(point1, point2):
    return geopy.distance.distance(point1, point2, ellipsoid="GRS-80").km

# %%
# # Read excel file
# file_path = r"D:\baseline creation\NETWORK COORDINATES.xlsx"


# # Assign excel file to panda dataframe
# df = pd.read_excel(file_path)
# # print(df)
# with open('df.pkl', 'rb') as f:
#     df = pickle.load(f)

def load_df():
    global df
    try:
        with open('df.pkl', 'rb') as f:
            df = pickle.load(f)
    except:
        file_path = r"NETWORK COORDINATES.xlsx"
        df = pd.read_excel(file_path)

    return df



# ectract long and lat from xcel file
def extract_long_lat():
    df = load_df()
    cluster_df = df[['Site Code', 'Lat dec', 'Long dec']]
    lo_la_df = df[['Lat dec', 'Long dec']]
# print(cluster_df)

# print(len(cluster_df))
# convert into list
    lo_la_list = lo_la_df.values.tolist()
    return lo_la_list
# print(lo_la_list)
# %%

# Clustering
def create_clusters():
    lo_la_list = extract_long_lat()
    X = np.array(lo_la_list)

    kmeans = KMeans(n_clusters=5, n_init='auto', random_state=0).fit(X)

    labels = kmeans.predict(X)
    # print(labels)
    regions = [0, 1, 2, 3, 4]
    region_0 = []
    region_1 = []
    region_2 = []
    region_3 = []
    region_4 = []


    # store the clusters into groups/variables
    for i in range(len(X)):
        if labels[i] == 0:
            region_0.append(X[i])
        elif labels[i] == 1:
            region_1.append(X[i])
        elif labels[i] == 2:
            region_2.append(X[i])
        elif labels[i] == 3:
            region_3.append(X[i])
        elif labels[i] == 4:
            region_4.append(X[i])
    # print(region_0)
    # print(region_1)
    # print(region_2)
    # print(region_3)
    # print(region_4)

    # create dataframes for the 5 clusters
    r0_df = pd.DataFrame(region_0, columns=['Lat dec', 'Long dec'])
    r1_df = pd.DataFrame(region_1, columns=['Lat dec', 'Long dec'])
    r2_df = pd.DataFrame(region_2, columns=['Lat dec', 'Long dec'])
    r3_df = pd.DataFrame(region_3, columns=['Lat dec', 'Long dec'])
    r4_df = pd.DataFrame(region_4, columns=['Lat dec', 'Long dec'])

    r0_df["Site Code"] = df["Site Code"]
    r1_df["Site Code"] = df["Site Code"]
    r2_df["Site Code"] = df["Site Code"]
    r3_df["Site Code"] = df["Site Code"]
    r4_df["Site Code"] = df["Site Code"]


    clusters = [r0_df, r1_df, r2_df, r3_df, r4_df]
    df_clusters = []
    selected_hubs = []
    site_code_dicts = []
    # print(r0_df)
    # print(r1_df)
    # print(r2_df)
    # print(r3_df)
    # print(r4_df)


    # compute distances within clusters, find average and sort means inascending order
    for sub_df in clusters:
        single_df = single_hub_df(df, sub_df)
        df_clusters.append(single_df)
        dist_summary = comp_distances(single_df, "NGS CORS", "Site Code")
        means = get_sorted_means(dist_summary)

        selected_single_hub = list(means.keys())[0]
        selected_hubs.append(selected_single_hub)

    # print(selected_hubs)


    # extract hubs from each cluster
    mask = df["Site Code"].isin(selected_hubs)
    new_df = df[mask]
    # print(new_df)
    return new_df, df_clusters, selected_hubs

# mask = df["Site Code"].isin(selected_hubs)
# new_df = df[mask]
# sorting_index = np.argsort(np.array(selected_hubs))
# new_df = new_df.iloc[sorting_index]
# print(new_df)


# %%

# Extract 4 of the least distance

# Create an empty list to store the distances
def get_distances():
    new_df, df_clusters, selected_hubs = create_clusters()
    distances = []

    # Iterate over the rows of the DataFrame
    for i, row in new_df.iterrows():
        # Calculate the distance to all other points
        for j, other_row in new_df.iterrows():
            if i != j:
                point1 = (row["Lat dec"], row["Long dec"])
                point2 = (other_row["Lat dec"], other_row["Long dec"])
                distance = calc_distance(point1, point2)
                distances.append(
                    (distance, row["Site Code"], other_row["Site Code"]))
                # print(distances)
    # Sort the list of distances in ascending order
    distances.sort()

    # Initialize a dictionary to store the selected distances
    selected_distances = {}

    # Initialize a counter to keep track of how many distances have been printed
    count = 0

    previous_start = None
    previous_end = None
    for distance, start, end in distances:
        if (start != end) and (start != previous_start or end != previous_end) and (start != previous_end or end != previous_start) and count < 4:
            # Add the distance to the dictionary
            selected_distances[f"{start} to {end}"] = distance
            count += 1
            previous_start = start
            previous_end = end

    # Print the selected distances
    # print(selected_distances)


    # Create an empty DataFrame with two columns: "start" and "end"
    hub_baselines_df = pd.DataFrame(columns=["start", "end"])

    # Iterate over the keys and values in the selected_distances dictionary
    for key, value in selected_distances.items():
        # Split the key string at the " to " string to extract the start and end point codes
        start, end = key.split(" to ")
        # Add a row to the DataFrame with the start and end point codes
        df_temp = pd.DataFrame({"start": [start], "end": [end]})
        hub_baselines_df = pd.concat(
            [hub_baselines_df, df_temp], ignore_index=True)
    
    return hub_baselines_df

# Print the DataFrame
# print(hub_baselines_df)


# %%

# #CREATE DICTIONARIES TO POPULATE XML
def create_xml_dict():
# SITE CODE DICTIONARY
    _, df_clusters, selected_hubs = create_clusters()
    r0_df_cluster = df_clusters[0]
    r1_df_cluster = df_clusters[1]
    r2_df_cluster = df_clusters[2]
    r3_df_cluster = df_clusters[3]
    r4_df_cluster = df_clusters[4]

    s0 = selected_hubs[0]
    s1 = selected_hubs[1]
    s2 = selected_hubs[2]
    s3 = selected_hubs[3]
    s4 = selected_hubs[4]

    site_code_dictionaries = []
    for i in range(5):
        df_cluster = eval(f"r{i}_df_cluster")
        selected_hub = eval(f"s{i}")
        code_df = df_cluster["Site Code"]
        code_dict = code_df.to_dict()

        value_to_remove = selected_hub
        keys_to_remove = []

        for key, value in code_dict.items():
            if value == value_to_remove:
                keys_to_remove.append(key)

        for one_key in keys_to_remove:
            code_dict.pop(one_key)

        # append the dictionary to the list
        site_code_dictionaries.append(code_dict)

    # print(site_code_dictionaries)  # print the list of dictionaries

    # SITE CODE DICTIONARY
    x0 = site_code_dictionaries[0]
    x1 = site_code_dictionaries[1]
    x2 = site_code_dictionaries[2]
    x3 = site_code_dictionaries[3]
    x4 = site_code_dictionaries[4]


    # CREATE DICTIONARY FOR HUBS
    true_df = df[df["NGS CORS"] == True]
    # print(true_df)
    for i in range(len(true_df)):
        cors_summary = true_df["Site Code"]
    # print(cors_summary)
    # print("_"*70 + "old CORS" + "_"*70)
    cors_dict = cors_summary.to_dict()

    # print(cors_dict)
    # print(len(cors_dict.items()))


    for value in [s0, s1, s2, s3, s4]:
        keys_to_remove = []
        for key, val in cors_dict.items():
            if val == value:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            cors_dict.pop(key)

    # print("_"*70 + "new CORS" + "_"*70)
    # print(cors_dict)
    # print(len(cors_dict.items()))
    # print(s0)
    return site_code_dictionaries, s0, s1, s2, s3, s4, cors_dict, site_code_dictionaries

# %%

# POPULATE OPUS PROJECT JOB INPUT FILE
def populate_xml():
# create root element
    _, _, selected_hubs = create_clusters()
    hub_baselines_df = get_distances()
    site_code_dictionaries, s0, s1, s2, s3, s4, cors_dict, site_code_dictionaries = create_xml_dict()
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
    for value in [s0, s1, s2, s3, s4]:
        hub1 = ET.SubElement(cors, 'HUB')
        hub1.text = value
        fix1 = ET.SubElement(hub1, 'FIX')
        fix1.text = '3-D'

    # CORS that are not hubs but must be included as well
    for key, value in cors_dict.items():
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
        dom.writexml(f, indent='  ', addindent='  ', newl='\n', encoding='utf-8')

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
    return filtered_s_hub_map_df, filtered_map_dfs, hub_connection_start_resulting_df, hub_connection_end_resulting_df


# %%
# map display
filtered_s_hub_map_df, filtered_map_dfs, hub_connection_start_resulting_df, hub_connection_end_resulting_df = populate_xml()

def create_default_map():
    # Create a map centered on the USA
    map = folium.Map(location=[38.0, -97.0], zoom_start=5)

    # Return the map
    return map


# %%
def create_five_hubs_map():
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

    for j in range(len(filtered_s_hub_map_df)):
        sub_df = filtered_map_dfs[j]
        end_coords = [filtered_s_hub_map_df.iloc[j]['Lat dec'], -
                      1 * abs(filtered_s_hub_map_df.iloc[j]['Long dec'])]
        for i, row in sub_df.iterrows():
            start_coords = [row['Lat dec'], -row['Long dec']]
            line = folium.PolyLine(
                locations=[start_coords, end_coords], color='blue', weight=2, opacity=1)
            line.add_to(polyline_layer)
            polyline_layer.add_to(map)

    # Iterate over the rows of hub_connection_start_resulting_df
    for i, row in hub_connection_start_resulting_df.iterrows():
        # Get the coordinates of the start marker
        start_coords = [row['Lat dec'], -row['Long dec']]
        # Get the coordinates of the end marker
        end_coords = [hub_connection_end_resulting_df.loc[i, 'Lat dec'], -
                      hub_connection_end_resulting_df.loc[i, 'Long dec']]
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
    map.save('map.html')

    return map

# print("Number of receivers: ", df.shape[0])
# print("Number of independent baselines: ", len(distances))
