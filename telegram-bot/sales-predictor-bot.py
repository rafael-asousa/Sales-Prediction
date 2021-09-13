import requests
import json
import pandas as pd
import os
from flask import Flask, request, Response

# constants
token = '1929459281:AAHeyV-oGTIFci2ezK8uELRpKpE3xVtdmkk'

#set webhook commnad
#https://api.telegram.org/bot1929459281:AAHeyV-oGTIFci2ezK8uELRpKpE3xVtdmkk/setWebhook?url=https://cdc04cda65be30.localhost.run


def send_message( chat_id, text ):
    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}'

    r = requests.post( url, json={'text': text } )
    print( 'Status Code {}'.format( r.status_code ) )

    return None


def parse_message( message ):
    chat_id = message['message']['chat']['id']
    store_id = message['message']['text']

    store_id = store_id.replace( '/', '' )

    try:
        store_id = int( store_id )

    except ValueError:
        store_id = 'error'

    return chat_id, store_id

def load_dataset( store_id ):
    
    dfx = pd.read_csv('../data/test.csv')
    df_raw_store = pd.read_csv('../data/store.csv', low_memory=False)
    dfx_complete = pd.merge(df_raw_store, dfx, how='left', on='Store')
    
    api_test_data = dfx_complete[dfx_complete['Store'] == store_id ]
    
    if not api_test_data.empty:
    
        api_test_data = api_test_data[api_test_data['Open'] != 0]
        api_test_data = api_test_data[~api_test_data['Open'].isnull()] #there are some NaN in Open column to get rid off
        api_test_data = api_test_data.drop('Id', axis=1)

        data_to_api = json.dumps( api_test_data.to_dict( orient='records' ) )

    else:
        data_to_api = 'error'
        
    return data_to_api

def predict( data ):
    r = requests.post( 'https://rafael-sales-predictor.herokuapp.com/sales_prediction/predict', data=data, headers={'Content-type': 'application/json' } )
    df = pd.DataFrame(r.json(), columns=r.json()[0].keys())
    
    return df


app = Flask( __name__ )

@app.route( '/', methods=['GET', 'POST'] )
def index():
    if request.method == 'POST':
        message = request.get_json()

        chat_id, store_id = parse_message( message )

        if store_id != 'error':
            # loading data
            data = load_dataset( store_id )

            if data != 'error':
                # prediction
                d1 = predict( data )

                # calculation
                d2 = d1[['store', 'prediction']].groupby( 'store' ).sum().reset_index()
                
                store_number = d2['store'].values[0]
                store_predictions = d2['prediction'].values[0]
                
                # send message
                msg = f'Store Number { store_number } will sell R${store_predictions:.2f} in the next 6 weeks'

                send_message( chat_id, msg )
                return Response( 'Ok', status=200 )

            else:
                send_message( chat_id, 'Store Not Available' )
                return Response( 'Ok', status=200 )

        else:
            send_message( chat_id, 'Store ID is Wrong' )
            return Response( 'Ok', status=200 )


    else:
        return '<h1> Rossmann Telegram BOT </h1>'
    


if __name__ == '__main__':
    port = os.environ.get( 'PORT', 5000 )
    app.run( host='0.0.0.0', port=port )
