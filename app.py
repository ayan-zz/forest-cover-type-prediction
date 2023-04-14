from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline

application=Flask(__name__)

app=application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=CustomData(
            Id=request.form.get('Id'),
            Elevation=int(request.form.get('Elevation')),
            Aspect=int(request.form.get('Aspect')),
            Slope=int(request.form.get('Slope')),
            Horizontal_Distance_To_Hydrology=int(request.form.get('Horizontal_Distance_To_Hydrology')),
            Vertical_Distance_To_Hydrology=int(request.form.get('Vertical_Distance_To_Hydrology')),
            Horizontal_Distance_To_Roadways=int(request.form.get('Horizontal_Distance_To_Roadways')),
            Hillshade_9am=int(request.form.get('Hillshade_9am')),
            Hillshade_Noon=int(request.form.get('Hillshade_Noon')),
            Hillshade_3pm=int(request.form.get('Hillshade_3pm')),
            Horizontal_Distance_To_Fire_Points=int(request.form.get('Horizontal_Distance_To_Fire_Points')),
            Wilderness=request.form.get('Wilderness'),
            Soil=request.form.get('Soil')
        )
        pred_df=data.get_data_as_dataframe()
        print(pred_df)

        predict_pipeline=PredictPipeline()
        result=predict_pipeline.predict(pred_df)

        categories={0.:'SPRUCE / FIR',1.:'LODGEPOLE PINE',2.:'PONDEROSA PINE',3.:'COTTONWOOD / WILLOW',
                    4.:'ASPEN',5.:'DOUGLAS-FIR',6.: 'Krummholz'}
        
        results = categories[result[0]]
        

        return render_template("home.html",results=results)

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True,port=5000)
    
    
    
