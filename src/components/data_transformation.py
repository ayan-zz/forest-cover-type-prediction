import os
import sys
import numpy  as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from dataclasses import dataclass
from src.utils import save_object

from src.exception import CustomException
from src.logger import logging

@dataclass
class DataConfigTransformation:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")

class DataTransform:
    def __init__(self):
        self.data_transformation_config=DataConfigTransformation()
    def get_transformer_object(self):
        try:
            numerical_columns=['Elevation', 'Aspect', 'Slope',
                               'Horizontal_Distance_To_Hydrology', 'Vertical_Distance_To_Hydrology',
                               'Horizontal_Distance_To_Roadways', 'Hillshade_9am', 'Hillshade_Noon',
                               'Hillshade_3pm', 'Horizontal_Distance_To_Fire_Points']
            cat_columns=['Wilderness', 'Soil']

            numerical_pipeline=Pipeline(steps=[("scaler",StandardScaler())])
            cat_column_pipeline=Pipeline(
                steps=[
                ("one_hot_encoder",OneHotEncoder(sparse=False, handle_unknown='ignore')),
                ("scaler",StandardScaler(with_mean=False))
                ])
                
            logging.info(f"Categorical columns: {cat_columns}")
            
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer([
                ("numerical_pipeline",numerical_pipeline,numerical_columns),
                ("cat_pipeline",cat_column_pipeline,cat_columns)])

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformer(self,train_path,test_path):
        try:
            df_train=pd.read_csv(train_path)
            df_test=pd.read_csv(test_path)

            logging.info("Read Train ans test data completed")
            logging.info("obtaining preprocesser object")

            preprocessor_obj=self.get_transformer_object()
            target_column_name="Cover_Type"
            
            numerical_columns=['Elevation', 'Aspect', 'Slope',
                              'Horizontal_Distance_To_Hydrology', 'Vertical_Distance_To_Hydrology',
                               'Horizontal_Distance_To_Roadways', 'Hillshade_9am', 'Hillshade_Noon',
                               'Hillshade_3pm', 'Horizontal_Distance_To_Fire_Points']
            df_train[numerical_columns]=abs(df_train[numerical_columns])
            df_test[numerical_columns]=abs(df_test[numerical_columns])

            le=LabelEncoder()
            df_train[target_column_name]=le.fit_transform(df_train[target_column_name])
            df_test[target_column_name]=le.transform(df_test[target_column_name])

            dff=np.where(df_train[numerical_columns]<0,0,df_train[numerical_columns])
            df_train[numerical_columns]=pd.DataFrame(dff, columns=numerical_columns)

            dtt=np.where(df_test[numerical_columns]<0,0,df_test[numerical_columns])
            df_test[numerical_columns]=pd.DataFrame(dtt, columns=numerical_columns)

            q1 = df_train[numerical_columns].quantile(0.25)
            q3 = df_train[numerical_columns].quantile(0.75)
            iqr = q3-q1
            med=df_train[numerical_columns].median()
            upper_bound = (q3+(1.5*iqr))
            lower_bound = (q1-(1.5*iqr))

            doo = np.where(df_train[numerical_columns] <=lower_bound,med,df_train[numerical_columns])
            doo1= np.where(df_train[numerical_columns] >=upper_bound,med,doo)
            df_train[numerical_columns]=pd.DataFrame(doo1, columns=numerical_columns)

            q11 = df_test[numerical_columns].quantile(0.25)
            q31 = df_test[numerical_columns].quantile(0.75)
            iqr1 = q31-q11
            med1=df_test[numerical_columns].median()
            upper_bound1 = (q31+(1.5*iqr1))
            lower_bound1 = (q11-(1.5*iqr1))

            d1 = np.where(df_test[numerical_columns] <=lower_bound1,med1,df_test[numerical_columns])
            d2= np.where(df_test[numerical_columns] >=upper_bound1,med1,d1)
            df_test[numerical_columns]=pd.DataFrame(d2, columns=numerical_columns)           


            target_feature_train_df=df_train[target_column_name]
            input_feature_train_df=df_train.drop(columns=['Cover_Type','Id'],axis=1)
             

            target_feature_test_df=df_test[target_column_name]
            target_feature_test_df=target_feature_test_df.astype(int)
            input_feature_test_df=df_test.drop(columns=['Cover_Type','Id'],axis=1)
        

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe.")

            input_feature_train_arr=preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessor_obj.transform(input_feature_test_df)       

            train_arr = np.c_[input_feature_train_arr, target_feature_train_df]
            test_arr = np.c_[input_feature_test_arr,target_feature_test_df]                 

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj
            )            
            
            return (train_arr,test_arr,self.data_transformation_config.preprocessor_obj_file_path)

        except Exception as e:
            raise CustomException(e,sys)
        

