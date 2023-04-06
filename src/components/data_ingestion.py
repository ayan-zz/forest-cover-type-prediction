import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransform
from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import ModelTrainerConfig
@dataclass
class DataIngestionConfig:
    train_data_path=os.path.join('artifacts',"train.csv")
    test_data_path=os.path.join('artifacts',"test.csv")
    raw_data_path=os.path.join('artifacts',"raw.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Initiate the data ingestion")

        try:
            df=pd.read_csv("notebook/data/forest.csv")
            soil_dummy = df.loc[:,df.columns.str.startswith('Soil_Type')]
            wild_dummy=df.loc[:,df.columns.str.startswith('Wilderness_Area')]
            wild = wild_dummy.idxmax(axis=1)
            soil = soil_dummy.idxmax(axis=1)
            wild.name = 'Wilderness'
            soil.name = 'Soil'
            df['Wilderness']= wild
            df['Soil'] = soil

            df.drop(columns=['Wilderness_Area1','Wilderness_Area2', 'Wilderness_Area3', 'Wilderness_Area4',
                             'Soil_Type1', 'Soil_Type2', 'Soil_Type3', 'Soil_Type4', 'Soil_Type5','Soil_Type7',
                             'Soil_Type6', 'Soil_Type8', 'Soil_Type9', 'Soil_Type10', 'Soil_Type11','Soil_Type15',
                             'Soil_Type12', 'Soil_Type13', 'Soil_Type14', 'Soil_Type16',
                             'Soil_Type17', 'Soil_Type18', 'Soil_Type19', 'Soil_Type20',
                             'Soil_Type21', 'Soil_Type22', 'Soil_Type23', 'Soil_Type24',
                             'Soil_Type25', 'Soil_Type26', 'Soil_Type27', 'Soil_Type28',
                             'Soil_Type29', 'Soil_Type30', 'Soil_Type31', 'Soil_Type32',
                             'Soil_Type33', 'Soil_Type34', 'Soil_Type35', 'Soil_Type36',
                             'Soil_Type37', 'Soil_Type38', 'Soil_Type39', 'Soil_Type40'], axis=1,inplace=True)
            
            logging.info("Read the dataset as dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42) 

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("data ingestion had completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )


        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_trans=DataTransform()
    train_arr,test_arr,_=data_trans.initiate_data_transformer(train_data,test_data)

    modeltrainer= ModelTrainer()
    print(modeltrainer.initate_training(train_arr,test_arr))
    



        

