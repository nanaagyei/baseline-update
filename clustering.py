from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import folium
from geopy import distance
import geopy.distance
from sklearn.neighbors import NearestNeighbors


#%%

# all functions:

def tuple_to_list(arr):
    my_list = [list(t) for t in arr]
    new_arr =  np.array(my_list)
    return new_arr

# slicing the df into a dataframe for each cluster
def single_hub_df(main_df, sub_df):
    mask = main_df["Lat dec"].isin(sub_df["Lat dec"]) & main_df["Long dec"].isin(sub_df["Long dec"])
    df_region = main_df[mask]
    return df_region

#function to compute distances
def comp_distances(df, column_name, index="Site Code"):
    df = df.reset_index(drop=True)
    true_df = df[df[column_name] == True].reset_index(drop=True)
    false_df=df[df[column_name] == False].reset_index(drop=True)
    dist = []
    true_dist = pd.DataFrame()
    for i in range(len(true_df[index])):
        for j in range(len(false_df[index])):
            trues = (true_df["Lat dec"][i], true_df["Long dec"][i])
            falses = (false_df["Lat dec"][j], false_df["Long dec"][j])
            dist.append(distance.distance(trues, falses, ellipsoid="GRS-80").km)
        true_dist[true_df[index][i]] = dist
        dist = []
    return true_dist.set_index(false_df[index])

#Sort the means
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
    false_df= df[df[column_name] == True].reset_index(drop=True)
    dist = []
    true_dist = pd.DataFrame()
    for i in range(len(true_df[index])):
        for j in range(len(false_df[index])):
            trues = (true_df["Lat dec"][i], true_df["Long dec"][i])
            falses = (false_df["Lat dec"][j], false_df["Long dec"][j])
            dist.append(distance.distance(trues, falses, ellipsoid="GRS-80").km)
        true_dist[true_df[index][i]] = dist
        dist = []
    return true_dist.set_index(false_df[index])

#%%
# Define a function to calculate the distance between two points
def calc_distance(point1, point2):
    return geopy.distance.distance(point1, point2,ellipsoid="GRS-80").km


#%%
# Read excel file
file_path = r"D:\baseline creation\NETWORK COORDINATES.xlsx"

# Assign excel file to panda dataframe
df = pd.read_excel(file_path)
# print(df)

#ectract long and lat from xcel file
cluster_df = df[['Site Code','Lat dec','Long dec']]
lo_la_df = df[['Lat dec','Long dec']]
# print(cluster_df)

# print(len(cluster_df))
#convert into list
lo_la_list = lo_la_df.values.tolist()
# print(lo_la_list)

#%%

# Clustering
X = np.array(lo_la_list)

kmeans = KMeans(n_clusters=5, n_init='auto', random_state=0).fit(X)

labels = kmeans.predict(X)
# print(labels)
regions = [0,1,2,3,4]
region_0 = []
region_1 = []
region_2 = []
region_3 = []
region_4 = []



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


r0_df = pd.DataFrame(region_0, columns =['Lat dec', 'Long dec'])
r1_df = pd.DataFrame(region_1, columns =['Lat dec', 'Long dec'])
r2_df = pd.DataFrame(region_2, columns =['Lat dec', 'Long dec'])
r3_df = pd.DataFrame(region_3, columns =['Lat dec', 'Long dec'])
r4_df = pd.DataFrame(region_4, columns =['Lat dec', 'Long dec'])
clusters = [r0_df, r1_df,r2_df,r3_df,r4_df]
df_clusters = []
selected_hubs = []
site_code_dicts = []
# print(r0_df)
# print(r1_df)
# print(r2_df)
# print(r3_df)
# print(r4_df)

# mask = df["Lat dec"].isin(r0_df["Lat dec"]) & df["Long dec"].isin(r0_df["Long dec"])

# df_r0 = df[mask]

# print(df_r0)
for sub_df in clusters:
    single_df = single_hub_df(df, sub_df)
    df_clusters.append(single_df)
    dist_summary = comp_distances(single_df,"NGS CORS","Site Code")
    # print("Distance Summary: ")
    # print(dist_summary)
    # print("="*70)
    means = get_sorted_means(dist_summary)
    # print("Means: ")
    # print(means)
    # print("="*70)
    selected_single_hub = list(means.keys())[0]
    selected_hubs.append(selected_single_hub)

# for i in range(len(df_clusters)):
#     site_code_df = df_clusters[i]["Site Code"]
#     site_code_dict = dict(site_code_df)
#     remove_selected_hub(site_code_dict, selected_hubs[i])
#     site_code_dicts.append(site_code_dict)

# for i in range(len(site_code_dicts)):
#     print("Selected Site Hubs: ")
#     print(selected_hubs[i])
#     print("="*70)
#     print("Site Code Dictionaries: ")
#     print(site_code_dicts[i])
#     print("Size of Dict: ", len(site_code_dicts[i]))
#     print("="*70)

mask = df["Site Code"].isin(selected_hubs)
new_df = df[mask]
print(new_df)




#%%
#__________________________________________________________________________________________________________________
# # Create an empty list to store the distances
# distances = []

# # Iterate over the rows of the DataFrame
# for i, row in new_df.iterrows():
#     # Calculate the distance to all other points
#     for j, other_row in new_df.iterrows():
#         if i != j:
#             point1 = (row["Lat dec"], row["Long dec"])
#             point2 = (other_row["Lat dec"], other_row["Long dec"])
#             distance = calc_distance(point1, point2)
#             distances.append((distance, row["Site Code"], other_row["Site Code"]))
#             # print(distances)
# # Sort the list of distances in ascending order
# distances.sort()

# # Initialize a dictionary to store the selected distances
# selected_distances = {}

# # Initialize a counter to keep track of how many distances have been printed
# count = 0

# previous_start = None
# previous_end = None
# for distance, start, end in distances:
#     if (start != end) and (start != previous_start or end != previous_end) and (start !=previous_end or end != previous_start ) and count < 4: 
#         # Add the distance to the dictionary
#         selected_distances[f"{start} to {end}"] = distance
#         count += 1
#         previous_start = start
#         previous_end = end

# # Print the selected distances
# print(selected_distances)




#%%
#_________________________________________________________________________________________________________________
cors_dist_summary = comp_cors_distances(new_df, "NGS CORS", "Site Code")
print(cors_dist_summary)
cors_means = get_sorted_means(cors_dist_summary)
print(cors_means)

# min_values = []


# # get a list of minimum values for each column in the dataframe
# for hub in selected_hubs:
#     mask = cors_dist_summary[hub] > 0
#     min_val = cors_dist_summary.loc[mask, hub].min()
#     min_values.append(min_val)
# print(min_values)

# indices = []

# for val in min_values:
#     row_index, col_index = cors_dist_summary.where(cors_dist_summary == val).stack().index[0]
#     indices.append((row_index, col_index))

# print(indices)



#______________________________________________________________________________________________________________________
# cors_df = new_df[['Site Code','Lat dec','Long dec']]
# cors_val_df = new_df[['Lat dec','Long dec']]

# cors_val_list = cors_val_df.values.tolist()

# X_cors = np.array(cors_val_list)

# nn = NearestNeighbors(n_neighbors=4)

# nn.fit(X_cors)

# # Compute the distances to the 4 nearest neighbors for each point
# distances, indices = nn.kneighbors()

# # Print the distances
# print(distances)
# print(indices)

#%%
# #Plot latitude and longitudes for each region

## region_0 = tuple_to_list(region_0)
# mean_lon = np.mean(region_0[:, 1])
# mean_lat = np.mean(region_0[:, 0])

# map1 = folium.Map(location=[mean_lat, -mean_lon], zoom_start=8)

# for i in range(len(region_0)):
#     lon = -region_0[i, 1]
#     lat = region_0[i, 0]
#     folium.Marker([lat,lon],icon=folium.Icon(color='red', icon='')).add_to(map1)
    
# # map1.save("index.html")

## region_1 = tuple_to_list(region_1)
# mean_lon = np.mean(region_1[:, 1])
# mean_lat = np.mean(region_1[:, 0])

# # map2 = folium.Map(location=[mean_lat, -mean_lon], zoom_start=8)
# folium.Map(location=[mean_lat, -mean_lon], zoom_start=8).add_to(map1)
# for i in range(len(region_1)):
#     lon = -region_1[i, 1]
#     lat = region_1[i, 0]
#     folium.Marker([lat,lon],icon=folium.Icon(color='green', icon='')).add_to(map1)

## region_2 = tuple_to_list(region_2)
# mean_lon = np.mean(region_2[:, 1])
# mean_lat = np.mean(region_2[:, 0])

# # map2 = folium.Map(location=[mean_lat, -mean_lon], zoom_start=8)
# folium.Map(location=[mean_lat, -mean_lon], zoom_start=8).add_to(map1)
# for i in range(len(region_2)):
#     lon = -region_2[i, 1]
#     lat = region_2[i, 0]
#     folium.Marker([lat,lon],icon=folium.Icon(color='blue', icon='')).add_to(map1)

## region_3 = tuple_to_list(region_3)
# mean_lon = np.mean(region_3[:, 1])
# mean_lat = np.mean(region_3[:, 0])

# # map2 = folium.Map(location=[mean_lat, -mean_lon], zoom_start=8)
# folium.Map(location=[mean_lat, -mean_lon], zoom_start=8).add_to(map1)
# for i in range(len(region_3)):
#     lon = -region_3[i, 1]
#     lat = region_3[i, 0]
#     folium.Marker([lat,lon],icon=folium.Icon(color='orange', icon='')).add_to(map1)
    
## region_4 = tuple_to_list(region_4)
# mean_lon = np.mean(region_4[:, 1])
# mean_lat = np.mean(region_4[:, 0])

# # map2 = folium.Map(location=[mean_lat, -mean_lon], zoom_start=8)
# folium.Map(location=[mean_lat, -mean_lon], zoom_start=8).add_to(map1)
# for i in range(len(region_4)):
#     lon = -region_4[i, 1]
#     lat = region_4[i, 0]
#     folium.Marker([lat,lon],icon=folium.Icon(color='purple', icon='')).add_to(map1)

# map1.save('index_1.html')