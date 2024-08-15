import geopy.distance
import pandas as pd

# Define a function to calculate the distance between two points
def calc_distance(point1, point2):
    return geopy.distance.distance(point1, point2,ellipsoid="GRS-80").km

# Read excel file
file_path = r"D:\baseline creation\NETWORK COORDINATES.xlsx"

# Assign excel file to panda dataframe
df = pd.read_excel(file_path)
# print(df)

df = df[df["NGS CORS"] == True]
print(df)
# Create an empty list to store the distances
distances = []

# Iterate over the rows of the DataFrame
for i, row in df.iterrows():
    # Calculate the distance to all other points
    for j, other_row in df.iterrows():
        if i != j:
            point1 = (row["Lat dec"], row["Long dec"])
            point2 = (other_row["Lat dec"], other_row["Long dec"])
            distance = calc_distance(point1, point2)
            distances.append((distance, row["Site Code"], other_row["Site Code"]))
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
    if (start != end) and (start != previous_start or end != previous_end) and (start !=previous_end or end != previous_start ) and count < 4: 
        # Add the distance to the dictionary
        print(f"Distance from {start} to {end}: {distance:.2f} km")
        # selected_distances[start] = end
        key = (start, end)
        selected_distances[key] = distance
        count += 1
        previous_start = start
        previous_end = end

# Print the selected distances
print(selected_distances)
        




