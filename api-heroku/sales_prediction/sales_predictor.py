import os
import inflection
import pandas as pd
import numpy as np
import datetime
import pickle

#Define the class that will be used for production

class sales_prediction():
    def __init__(self):
        self.home_path = os.getcwd()
        self.competition_distance_scale =   pickle.load( open(os.path.join(self.home_path,'competition_distance_scale.pkl'), 'rb'))
        self.competition_open_since_scale = pickle.load( open(os.path.join(self.home_path,'competition_open_since_scale.pkl'), 'rb'))
        self.year_scale =                   pickle.load( open(os.path.join(self.home_path,'year_scale.pkl'), 'rb'))
        self.promo2_since_in_week_scale =   pickle.load( open(os.path.join(self.home_path,'promo2_since_in_week_scale.pkl'), 'rb'))
        self.store_type_encoder=            pickle.load( open(os.path.join(self.home_path,'store_type_encoder.pkl'), 'rb'))
    
    def cleaning(self, df):
        
        cols = df.columns
        snakecase_function = lambda x: inflection.underscore( x )
        cols_new = list( map(snakecase_function, cols) )
        df.columns = cols_new
        df = df.rename(columns={'promo_interval':'promo2_interval'})
        
        df['date'] = pd.to_datetime( df['date'] )
        
        df['competition_distance'] = df['competition_distance'].apply(lambda x: 300000 if np.isnan( x ) else x )

        df['competition_open_since_month'] = df.apply( lambda x: x['date'].month 
                                                        if np.isnan(x['competition_open_since_month']) 
                                                        else x['competition_open_since_month'], axis=1)

        df['competition_open_since_year'] = df.apply( lambda x: x['date'].year 
                                                       if np.isnan(x['competition_open_since_year']) 
                                                       else x['competition_open_since_year'], axis=1)

        df['promo2_since_week'] = df.apply( lambda x: x['date'].week 
                                             if np.isnan(x['promo2_since_week']) 
                                             else x['promo2_since_week'], axis=1)

        df['promo2_since_year'] = df.apply( lambda x: x['date'].year 
                                             if np.isnan(x['promo2_since_year']) 
                                             else x['promo2_since_year'], axis=1)

        df['promo2_interval'].fillna(0, inplace=True)

        months = ('Jan', 'Feb', 'Mar', 'Apr', 'May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
        month_map = {i+1: months[i] for i in range(12)}

        df['date_month'] = df['date'].dt.month.map( month_map )

        df['is_promo2'] = df[['date_month', 'promo2_interval']].apply(lambda x: 0 if x['promo2_interval'] == 0 else 
                                                                       1 if x['date_month'] in x['promo2_interval'].split(',') 
                                                                       else 0, axis=1 )
        
        df = df.astype( {'competition_open_since_month':'int64',
                         'competition_open_since_year':'int64',
                         'promo2_since_week':'int64',
                         'promo2_since_year':'int64'} )
        
        df = df[(df['open'] != 0)]
        
        cols_to_drop = ['open', 'promo2_interval', 'date_month']

        df = df.drop(cols_to_drop, axis = 1)
        
        return df
        
        
    def feature_engineering(self, df):
        
        df['year'] = df['date'].dt.year

        df['day'] = df['date'].dt.day

        df['weekofyear'] = df['date'].dt.isocalendar().week

        df['month'] = df['date'].dt.month

        df['year_week'] = df['date'].dt.strftime( '%Y-%W' )

        df['competition_open_date'] = df[['competition_open_since_month', 'competition_open_since_year']].apply(
                                    lambda x: datetime.datetime(year=x['competition_open_since_year'], month=x['competition_open_since_month'], day=1), axis=1 )

        df['competition_open_since'] = (df['date'] - df['competition_open_date']).dt.days

        df['promo2_since'] = df['promo2_since_year'].astype( str ) + '-' + df['promo2_since_week'].astype( str )
        df['promo2_since'] = df['promo2_since'].apply( lambda x: datetime.datetime.strptime( x + '-1', '%Y-%W-%w' ) - datetime.timedelta( days=7 ) )
        df['promo2_since_in_week'] = ( ( df['date'] - df['promo2_since'] )/7 ).apply( lambda x: x.days ).astype( int )

        df['assortment'] = df['assortment'].apply( lambda x: 'basic' if x == 'a' else 'extra' if x == 'b' else 'extended' )

        df['state_holiday'] = df['state_holiday'].apply( lambda x: 'public_holiday' if x == 'a' else 'easter_holiday' if x == 'b' else 'christmas' if x == 'c' else 'regular_day' )
        
        return df
        
    def preparation(self, df):
        
        df['competition_distance'] =   self.competition_distance_scale.transform( df[['competition_distance']].values )
        df['competition_open_since'] = self.competition_open_since_scale.transform( df[['competition_open_since']].values )
        df['year'] =                   self.year_scale.transform( df[['year']].values )
        df['promo2_since_in_week'] =   self.promo2_since_in_week_scale.transform( df[['promo2_since_in_week']].values )
        
        df = pd.get_dummies( df, prefix=['state_holiday'], columns=['state_holiday'] )

        df['store_type'] = self.store_type_encoder.transform( df['store_type'] )

        assortment_dict = {'basic': 1,  'extended': 2, 'extra': 3}
        df['assortment'] = df['assortment'].map( assortment_dict )

        df['day_of_week_sin'] = df['day_of_week'].apply( lambda x: np.sin( x * ( 2. * np.pi/7 ) ) )
        df['day_of_week_cos'] = df['day_of_week'].apply( lambda x: np.cos( x * ( 2. * np.pi/7 ) ) )

        df['month_sin'] = df['month'].apply( lambda x: np.sin( x * ( 2. * np.pi/12 ) ) )
        df['month_cos'] = df['month'].apply( lambda x: np.cos( x * ( 2. * np.pi/12 ) ) )

        df['day_sin'] = df['day'].apply( lambda x: np.sin( x * ( 2. * np.pi/30 ) ) )
        df['day_cos'] = df['day'].apply( lambda x: np.cos( x * ( 2. * np.pi/30 ) ) )

        df['week_of_year_sin'] = df['weekofyear'].apply( lambda x: np.sin( x * ( 2. * np.pi/52 ) ) )
        df['week_of_year_cos'] = df['weekofyear'].apply( lambda x: np.cos( x * ( 2. * np.pi/52 ) ) )
        
        cols_selected_model =[ 'store',
                               'store_type',
                               'assortment',
                               'competition_distance',
                               'promo2',
                               'promo',
                               'competition_open_since',
                               'promo2_since_in_week',
                               'day_of_week_sin',
                               'day_of_week_cos',
                               'month_sin',
                               'month_cos',
                               'day_sin',
                               'day_cos',
                               'week_of_year_sin',
                               'week_of_year_cos']
        
        return df[cols_selected_model]
    
    #data is what I receive from the user, data_to_predict is the transformed dataframe used for prediction    
    def get_prediction(self, model, data, data_to_predict):
        
        prediction         = model.predict( data_to_predict )
        data['prediction'] = np.expm1(prediction)
        
        return data.to_json( orient='records', date_format='iso' )
