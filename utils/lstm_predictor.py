import numpy as np
import  tensorflow
import sklearn
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM,Dense,Dropout


class StockPredictor:
    def __init__(self, model_path, price_data):
        self.model = load_model(model_path)
        self.data = price_data[['Close']].copy()
        self.scaler = MinMaxScaler()
        self.scaler.fit(self.data)

    def predict_next_day(self):
        last_50 = self.data['Close'].values[-50:].reshape(-1, 1)
        scaled = self.scaler.transform(last_50).reshape(1, 50, 1)
        pred_scaled = self.model.predict(scaled, verbose=0)[0, 0]
        return self.scaler.inverse_transform([[pred_scaled]])[0, 0]
    
    
    
    def predict_multiple_days(self, days=2):
        predictions = []
        last_50_days = self.data['Close'].values[-50:].reshape(-1, 1)
        last_50_scaled = self.scaler.transform(last_50_days)

        for _ in range(days):
            input_data = last_50_scaled.reshape(1, 50, 1)
            next_pred_scaled = self.model.predict(input_data)[0, 0]
            next_pred = self.scaler.inverse_transform([[next_pred_scaled]])[0, 0]
            predictions.append(next_pred)

            next_pred_scaled_array = np.array([[next_pred_scaled]])
            last_50_scaled = np.append(last_50_scaled[1:], next_pred_scaled_array).reshape(-1, 1)

        return predictions

    
    def get_last_actual_and_predictions(self):
        """Returns the last actual closing price and the next two predicted closing prices."""
        last_actual = self.data['Close'].iloc[-1]
        predictions = self.predict_multiple_days(days=2)
        return last_actual, predictions
    
    def recommend(self, risk_profile):
        last_actual, predicted_prices = self.get_last_actual_and_predictions()
        p0 = last_actual
        p1 = predicted_prices[0]
        p2 = predicted_prices[1]

        if p1 > p0 and p2 > p1:
            action = "BUY"
        elif p1 > p0 and p2 < p1:
            if p2 < p0:
                action = "HOLD"
            else:
                action = "BUY and SELL next day" if risk_profile == "high" else "HOLD"
        elif p1 < p0 and p2 < p1:
            action = "SELL"
        elif p1 < p0 and p2 > p1:
            if p2 > p0:
                action = "BUY"
            else:
                action = "BUY and SELL next day" if risk_profile == "high" else "HOLD"
        else:
            action = "HOLD"

        return action

