import pandas as pd
import numpy as np
from urllib.parse import urlparse
from IPython.display import display
from IPython.display import display
from sklearn.preprocessing import OneHotEncoder
import binascii
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score





class Prediction:


    def __init__(self):
        # read data from dataset file and convert to DataFrame format
        data_set = pd.read_csv('set.csv')
        ##   Assume that phishing, defacement and malware categories are bad (assign 0)
        ##  benign is good -> assign 0
        ##   phishing - 0
        ##   benign - 1
        ##   defacement - 0
        ##   malware - 0
        ##
        # create a dictionary for site types with corresponding values (0 or 1)
        dictionary_for_types = {'phishing' : 0, 'benign' : 1, 'defacement' : 0, 'malware' : 0}
        # replace object values (written with characters) with numbers 0 or 1 - in the type field
        data_set['type'] = data_set['type'].replace(dictionary_for_types)
        # create a new field in DataFrame 'parsed_url'
        #and apply parsing function to all values in a 'url' field
        data_set['parsed_url'] = data_set['url'].apply(self.parse_url)
        # Create 4 new fields in a DataFrame: scheme, domain, path, and query
        # apply lambda function: if there is no value in a field of parsed url,
        # fill that cell with 'none'
        data_set['scheme'] = data_set['parsed_url'].apply(lambda x: x.scheme if x.scheme else 'nothing')
        data_set['domain'] = data_set['parsed_url'].apply(lambda x: x.netloc if x.netloc else 'nothing')
        data_set['path'] = data_set['parsed_url'].apply(lambda x: x.path if x.path else 'nothing')
        data_set['query'] = data_set['parsed_url'].apply(lambda x: x.query if x.query else 'nothing')
        # delete a field 'url' and 'parsed_url' from DataFrame
        data_set = data_set.drop(['url', 'parsed_url'], axis=1)
        # create features X, which are the parameters, by which we judge the maliciousness
        # of websites
        X = data_set[['scheme', 'domain', 'path', 'query']]
        # encode the contents into numeric values
        X = X.applymap(self.hash_everything)
        # create a target variable y which provides an answer for the training/testing sets
        # (benign or not benign)
        y = data_set['type']
        # Separate our X and y into two sets: training set and testing set
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)


        # initialize a model which will use Logistic Regression
        self.model = LogisticRegression(max_iter=1000)

        # train the model using training sets
        self.model.fit(self.X_train, self.y_train)





    # function which parses the url
    # returns parsed url
    def parse_url(self, url):
        parsed_url = urlparse(url)
        return parsed_url

    # this function encodes the passed parameter
    # into numeric code, returns int value
    def hash_everything(self, cell):
        text_bytes = bytes(cell, 'utf-8')
        return int(binascii.crc32(text_bytes))

    def check_accuracy(self):
        # test the model, record answers in y_pred set
        self.y_pred = self.model.predict(self.X_test)

        # determine the accuracy of the model
        self.accuracy = accuracy_score(self.y_test, self.y_pred)
        self.accuracy = float("{0:.3g}".format(self.accuracy))


    def classify_website(self, url_to_test):

        # create a dictionary for a url
        data = {'url': [url_to_test]}
        # convert dictionary to DataFrame format
        test_data = pd.DataFrame(data)


        # parse url, prepare this DataFrame object for machine learning analysis
        test_data['parsed_url'] = test_data['url'].apply(self.parse_url)
        test_data['scheme'] = test_data['parsed_url'].apply(lambda x: x.scheme if x.scheme else 'nothing')
        test_data['domain'] = test_data['parsed_url'].apply(lambda x: x.netloc if x.netloc else 'nothing')
        test_data['path'] = test_data['parsed_url'].apply(lambda x: x.path if x.path else 'nothing')
        test_data['query'] = test_data['parsed_url'].apply(lambda x: x.query if x.query else 'nothing')

        test_data = test_data.drop(['url', 'parsed_url'], axis=1)

        # create what we will feed the model
        test_data = test_data[['scheme', 'domain', 'path', 'query']]

        # encode test data
        encoded_test_data = test_data.applymap(self.hash_everything)

        # make a prediction
        prediction = self.model.predict(encoded_test_data)
        return prediction
