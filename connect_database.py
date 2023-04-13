from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

cloud_config= {
  'secure_connect_bundle': 'C:\\Users\\Lenovo\\Downloads\\ML project\\forest\\secure-connect-forest-cover (1).zip'
}
auth_provider = PlainTextAuthProvider('sZcGEtTmAmmNJszRYHvvkBIN', 'ymnH,SGYC6a_P,,ROSW.Zl0uMhLvbezMLORDrRIvtpH_bZK-93N4w4q90xTPx_TecP7r-lnqpekGcNtB9Fdp3WzFNz-vtwD3K8Gf,JCHbdf4ZWe1YZ9Zb,HKUWCBe5-H')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect("machine_learning")

columns=["Id", "Aspect", "Cover_Type", "Elevation", "Hillshade_3pm", 
"Hillshade_9am", "Hillshade_Noon", "Horizontal_Distance_To_Fire_Points", 
"Horizontal_Distance_To_Hydrology", "Horizontal_Distance_To_Roadways", "Slope",
"Soil_Type1", "Soil_Type10", "Soil_Type11", "Soil_Type12", "Soil_Type13", "Soil_Type14", 
"Soil_Type15", "Soil_Type16", "Soil_Type17", "Soil_Type18", "Soil_Type19", "Soil_Type2", 
"Soil_Type20", "Soil_Type21", "Soil_Type22", "Soil_Type23", "Soil_Type24", "Soil_Type25", 
"Soil_Type26", "Soil_Type27", "Soil_Type28", "Soil_Type29", "Soil_Type3", "Soil_Type30", 
"Soil_Type31", "Soil_Type32", "Soil_Type33", "Soil_Type34", "Soil_Type35", "Soil_Type36", 
"Soil_Type37", "Soil_Type38", "Soil_Type39", "Soil_Type4", "Soil_Type40", "Soil_Type5", 
"Soil_Type6", "Soil_Type7", "Soil_Type8", "Soil_Type9", "Vertical_Distance_To_Hydrology",
"Wilderness_Area1", "Wilderness_Area2", "Wilderness_Area3", "Wilderness_Area4"]

row = session.execute("SELECT * FROM forest")
import pandas as pd
all=[]
for i in row:
    data_all=i
    data_all=list(data_all)
    all.append(data_all)
df=pd.DataFrame(all,columns=columns)


target_col=df['Cover_Type']
df_1=df.drop(columns=['Cover_Type'])
df_1['Cover_Type']=target_col

print(df_1.shape)

df_1.to_csv(r'C:\\Users\\Lenovo\\Downloads\\ML project\\forest\\notebook\\data\\data.csv')

