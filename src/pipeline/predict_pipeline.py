import sys,os
import pandas as pd
from src.exception import CustomException
from src.utils import load_object



class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path=os.path.join('artifacts','model.pkl')
            preprocessor_path=os.path.join('artifacts','preprocessor.pkl')
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            data_scaled=preprocessor.transform(features)
            preds=model.predict(data_scaled)
            return preds
        
        except Exception as e:
              raise CustomException(e,sys)

class CustomData:
    def __init__(self, 
                 Id : int,
                 Elevation :int,
                 Aspect: int,
                 Slope: int,
                 Horizontal_Distance_To_Hydrology: int,
                 Vertical_Distance_To_Hydrology: int,
                 Horizontal_Distance_To_Roadways: int,
                 Hillshade_9am: int,
                 Hillshade_Noon: int,
                 Hillshade_3pm: int,
                 Horizontal_Distance_To_Fire_Points: int,
                 Wilderness: str,
                 Soil: str):

                 self.Id =Id
                 self.Elevation = Elevation
                 self.Aspect = Aspect
                 self.Slope = Slope
                 self.Horizontal_Distance_To_Hydrology=Horizontal_Distance_To_Hydrology
                 self.Vertical_Distance_To_Hydrology=Vertical_Distance_To_Hydrology
                 self.Horizontal_Distance_To_Roadways=Horizontal_Distance_To_Roadways
                 self.Hillshade_9am = Hillshade_9am
                 self.Hillshade_Noon= Hillshade_Noon
                 self.Hillshade_3pm= Hillshade_3pm
                 self.Horizontal_Distance_To_Fire_Points=Horizontal_Distance_To_Fire_Points
                 self.Wilderness=Wilderness
                 self.Soil=Soil
                
    
    def get_data_as_dataframe(self):
          try:
                custom_data_input_dict={
                      "Id":[self.Id], "Elevation":[self.Elevation],
                      "Aspect":[self.Aspect],"Slope":[self.Slope],
                      "Horizontal_Distance_To_Hydrology":[self.Horizontal_Distance_To_Hydrology],
                      "Vertical_Distance_To_Hydrology":[self.Vertical_Distance_To_Hydrology],
                      "Horizontal_Distance_To_Roadways":[self.Horizontal_Distance_To_Roadways],
                      "Hillshade_9am":[self.Hillshade_9am],"Hillshade_Noon":[self.Hillshade_Noon],
                      "Hillshade_3pm": [self.Hillshade_3pm],"Horizontal_Distance_To_Fire_Points":[self.Horizontal_Distance_To_Fire_Points],
                      "Wilderness": [self.Wilderness],"Soil":[self.Soil]           
                }
                return pd.DataFrame(custom_data_input_dict)
          
          except Exception as e:
                raise CustomException(e,sys)
          


    

