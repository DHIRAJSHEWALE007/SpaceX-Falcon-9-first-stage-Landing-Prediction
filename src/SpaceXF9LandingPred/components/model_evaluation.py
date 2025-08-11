import pandas as pd
import numpy as np

from SpaceXF9LandingPred.logging import logger

from SpaceXF9LandingPred.entity import ModelEvaluationConfig

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier



class ModelEvaluation:
    def __init__(self, config:ModelEvaluationConfig, params):
        self.config=config
        self.params=params
        self.scaler=StandardScaler()

    def evaluate_models(self):

        data = pd.read_csv(self.config.data_path)
        X = data.drop(columns=['Class'], axis=1)
        Y = data['Class'].to_numpy()

        X = self.scaler.fit_transform(X)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=2)

        results={"Models":[],
                 "Accuracy Score":[]}

        models=[LogisticRegression(), SVC(), DecisionTreeClassifier(), KNeighborsClassifier()]
        
        for model in models:
            mdl=model
            model_name=mdl.__class__.__name__
            parameters=dict(self.params[model_name.lower()])
            cv=GridSearchCV(mdl, parameters, cv=10)
            cv.fit(X_train, Y_train)
            accuracy=cv.score(X_test, Y_test)
            results["Models"].append(model_name)
            results["Accuracy Score"].append(accuracy)

        result_df=pd.DataFrame(results)

        result_df.to_csv(self.config.evaluation_result_path, index=False)

        logger.info("Model Evaluation results are saved in artifacts")