import os
import json
import pandas as pd

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "models/DTC_6-4_7_6_no_scale.joblib"
)


class DetectModel:
    """Wrapper for loading and serving pre-trained model"""

    def __init__(self):
        self.model = self._load_model_from_path(MODEL_PATH)

    @staticmethod
    def _load_model_from_path(path):
        import joblib

        model = joblib.load(path)
        return model

    @staticmethod
    def preprocessor(message):
        dict_values: dict = json.loads(message)
        params = list(dict_values.values())
        print(params)
        return params

    def predict(self, message):
        """
        Make batch prediction on list of preprocessed feature dicts.
        Returns class probabilities if 'return_options' is 'Prob', otherwise returns class membership predictions
        """
        params = self.preprocessor(message)
        label = self.model.predict([params])[0]
        spam_prob = self.model.predict_proba([params])
        return {"label": int(label), "usefull_probability": float(spam_prob[0][1])}
