# Sales-Prediction: Predicting Sales for Drug Stores
Portfolio project for the prediction of sales for multiple drug stores.

# 1. Business Problem.

In order to properly allocate budget for projects in a series of drug stores, it is asked to make a prediction about how much each of a list of 1105 stores would sell in the next 6 weeks.

# 2. Business Assumptions.

1. I am assuming that predicting the sales for the next 6 weeks will actually be a solution to the problem the stakeholder has. I only have access to the dataset and not to the reasons behind the prediction.
2. I am assumin 'Sales' columns indicated in the dataset is in Reais (R$), brazilian currency. It is not clear if this data indicates a count of sales or the money spent on the store on the given day. I chose to treat it as money.
3. I have no access to the nature of promo1 and promo2, so I will consider that it makes sense that both promotions are applied at the same time with additive effects. (For example, it doesn't affect the price of the same products.)

# 3. Solution Strategy

The core idea for the solution strategy is to train a regression algorithm to act as a multivariate time series prediction To achieve this result, the following steps were taken:

### Part 1: Understanding the Data.

<b>Step 1:</b> Describe the data in size, columns, etc. Deal with NaN values. Use basic concepts of descriptive statistics, identify basic behavior of values and outliars, etc. 
<b>Step 2:</b> Construct a set of hypothesis of features that should affect our sales and make a feature enginnering in order to be able to check the hypothesis.
<b>Step 3:</b> Filter data to avoid data leakage and unuseful data.
<b>Step 4:</b> Make a Exploratory Data Analysis (EDA) in order to validate the hypothesis constructed in <b>Step 2</b> to gain understanding about the business.

### Part 2: Treat the data.

<b>Step 1:</b> Rescale, normalization, transformation and encoding of the data to increase the models capability of learning from our dataset.
<b>Step 2:</b> Feature selection using an algorithm (Boruta) and knowledge obtained from EDA.


### Part 3: Create and evaluate a Machine Learning Model.

<b>Step 1:</b> Define a baseline model to be compared to the trained algorithms. 
<b>Step 2:</b> Select a bunch of ML algorithms to evaluate the performance.
<b>Step 3:</b> Choose and validate the model that will be used based on characteristics like cross validation performance, deploy cost, value added to business, etc.
<b>Step 4:</b> Perform a Fine Tuning search for model hyperparameters
<b>Step 5:</b> Evaluate the model's performance in terms of business metrics and how it affects business decisions.

### Part 4: Deploy the model.

<b>Step 1:</b> An API was constructed in order to access the predictions for a given store.
<b>Step 2:</b> A telegram bot was constructed in order to allow the predictions to be accessible from a smartphone from anywhere in the world.

# 4. Top 3 Data Insights

1. Even though those data are from a Drug Store, it does not behave so differently from a regular store. For example, it sells more close to payment days (days 15 and 30), it sells more on hollidays, etc.
2. Competition is only a problem for sales after some time it opened. This probably means that drug stores need to build confidence from clients.
3. Promotions are not directly related to higher sales, the nature of the promotion is more important.

# 5. Machine Learning Model Applied

Tests were made for four machine learning models: Linear Regression, Regularized Linear Regression, Random Forest and XGBoost. Clearly the performance of XGBoost and Random Forest were the best ones, close to 15% mean percentage absolute error (MAPE). XGBoost was chosen to carry on analysis because the size of a trained random forest was limiting due to the costs for deploy.

# 6. Machine Learning Model Performance

| Model Name    | MAE                | MAPE          | RMSE               |
|:--------------|:-------------------|:--------------|:-------------------|
| XGBoost       | 1119.89 +/- 175.64 | 0.15 +/- 0.01 | 1619.54 +/- 247.25 |

# 7. Business Results

Those are the predictions summed for the total sales of all stores in next six weeks. The estimative is of about R$280 million with an estimated error of R$35 million up or down.

| predictions    | MAE                | best_scenario  | worst_scenario |
|:---------------|:-------------------|:---------------|:---------------|
| 278,809,600.00 | 34,573,524.97      | 313,383,129.35 | 244,236,079.40 |

# 8. Conclusions

A machine learning model was developed in order to predict the sales from multiple drug stores. With the use of XGBoost model it was possible to predict the sales from said stores for the next six weeks, with an estimated error of +/- 15%, in R$ 278,809,600.00. 

# 9. Lessons Learned

This was my first machine learning project, so the lessons I learned here are much more extense than it would be possible to summarize in t his brief section. However, I would like to highlight a few:

1. The importance of descriptive statistics through the process of training an algorithm.
2. How important it is to be able to relate the project you are doing with the business where it arises. This avoids problems as data leakage, lack of data, confidentiality, etc.
3. Business can be very tricky, the realization that drug stores sells are not related to sickness was honestly mind blowing.

# 10. Next Steps to Improve

In order to improve the project further, I would revisit every section and ask myself what I could do better. Here are a few answers I already found for myself while developing the projected but have not implemented yet:

1. If possible, get more data from stores. A few ones that I could think of is geographical data, like city, country, greenwhich zone, things like that.
2. Test different encodings for the categorical variables as there was no process of selection for the encoding method. Store maybe could have better encoding, for example.
3. Try to use different data spaces for the training, like PCA, t-SNE, etc.
