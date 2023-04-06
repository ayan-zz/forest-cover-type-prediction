import os
import sys
import numpy as np
import pandas as pd
from dataclasses import dataclass
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
from src.utils import save_object,evaluate_model
from src.exception import CustomException
from src.logger import logging


@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
    
    def initate_training(self, train_array,test_array):
        try:
            logging.info("splitting training and test imput data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1])
            models={
                "LogisticRegression":LogisticRegression(),
                "RandomForest": RandomForestClassifier(),
                "KNN": KNeighborsClassifier(),
                "xgboost":XGBClassifier()
            }
            params={
                "LogisticRegression":{'max_iter':[1000] },
                "RandomForest":{'n_estimators': [8,16,32,64]},
                "KNN":{'n_neighbors':[8,48,52,84]},
                "xgboost":{'n_estimators': [16,48,72,96], 'learning_rate':[0.01,0.01],'max_depth':[3]}
            }

            model_report:dict=evaluate_model(X_train=X_train,y_train=y_train,
                                             X_test=X_test,y_test=y_test,models=models,param=params)
            
            best_model_score = max(sorted(model_report.values()))

            best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model=models[best_model_name]

            if best_model_score<0.7:
                raise CustomException("No best model found")
            
            logging.info(f"Best found model on both training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model)
            
            predicted=best_model.predict(X_test)

            AccuracyScore= accuracy_score(y_test,predicted)
            classification_rep= classification_report(y_test,predicted)

            return (best_model_name,AccuracyScore)


        except Exception as e:
            raise CustomException (e,sys)