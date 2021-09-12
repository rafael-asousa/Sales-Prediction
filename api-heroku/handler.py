from flask import Flask, request, Response
import pickle
from sales_prediction.sales_predictor import sales_prediction
import pandas as pd
import os

model = pickle.load( open('model_xgb_trained.pkl', 'rb') )

app = Flask(__name__)

@app.route( '/sales_prediction/predict', methods=['POST'] )
def predict_sales():
    data_to_predict_json = request.get_json()
    
    if data_to_predict_json:
        if isinstance( data_to_predict_json, dict ): # unique example
            raw_data = pd.DataFrame( data_to_predict_json, index=[0] )
            
        else: # multiple example
            raw_data = pd.DataFrame( data_to_predict_json, columns=data_to_predict_json[0].keys() )
            
        pipeline = sales_prediction()
        
        # data cleaning
        df = pipeline.cleaning( raw_data )
        
        # feature engineering
        df = pipeline.feature_engineering( df )
        
        # data preparation
        df = pipeline.preparation( df )
        
        # prediction
        df_response = pipeline.get_prediction( model, raw_data, df )
        
        return df_response
    
    else:
        return Reponse( '{}', status=200, mimetype='application/json' )
    

    
if __name__ == '__main__':
    PORT = os.environ.get('PORT', 5000)
    app.run( host='0.0.0.0', port=PORT )
