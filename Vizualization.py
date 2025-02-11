#pip install geopandas pandas folium matplotlib
import pandas as pd
import folium

file_path = "/workspaces/BuffalizationChallenge/Data_Viz_Challenge_2025-UCB_Trees.csv"
df = pd.read_csv(file_path)

# Normalize to avoid huge or tiny dots
max_canopy = df["Canopy Spread"].max()
max_height = df["Height"].max()

# CU Boulder lat and long
m = folium.Map(location=[40.0076, -105.2659], zoom_start=16)

for _, row in df.iterrows():
    tree_type = row["Tree Type"].strip().upper()
    
    # Scale radius using a weighted average of Canopy Spread and Height
    if pd.notna(row["Canopy Spread"]) and pd.notna(row["Height"]): 
        radius = (row["Canopy Spread"] / max_canopy) * 5 + (row["Height"] / max_height) * 3
    else:
        radius = 3  
    
    # popup
    popup_text = f"""
    <b>Common Name:</b> {row['Common Name']}<br>
    <b>Tree Type:</b> {row['Tree Type']}<br>
    <b>Genus:</b> {row['Genus']}<br>
    <b>Species:</b> {row['Species']}<br>
    <b>Canopy Spread:</b> {row['Canopy Spread']} m<br>
    <b>Height:</b> {row['Height']} m
    """

   
    if tree_type == "DECIDUOUS":
        # Circle Marker for Deciduous Trees
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=radius,
            color="green",
            fill=True,
            fill_color="green",
            fill_opacity=0.7,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(m)
    
    elif tree_type == "CONIFEROUS":
        # Triangle Marker for Coniferous Trees
        folium.RegularPolygonMarker(
            location=[row["Latitude"], row["Longitude"]],
            number_of_sides=3,
            radius=radius,
            color="green",
            fill=True,
            fill_color="green",
            fill_opacity=0.7,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(m)

m.save("CU_Boulder_Tree_Map.html")

m