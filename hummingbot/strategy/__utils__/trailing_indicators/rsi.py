# Import necessary libraries
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator

# Define a class for the RSI Calculator
class RSICalculator:
    # Constructor method with a default period of 14
    def __init__(self, period=14):
        self.period = period  # Set the period for RSI calculation
        self.prices = []  # Initialize an empty list to store price data

    # Method to update the price list with the latest price
    def update_price(self, price):
        self.prices.append(price)  # Append the new price to the list
        # If the list of prices exceeds the period + 1, remove the oldest price
        if len(self.prices) > self.period + 1:
            self.prices.pop(0)

    # Method to calculate the current RSI value
    def calculate_rsi(self):
        # If there are not enough prices to calculate RSI, return None
        if len(self.prices) < self.period + 1:
            return None

        # Create a pandas DataFrame with the price data
        data = pd.DataFrame(self.prices, columns=['close'])
        # Create an RSIIndicator object using the ta library
        rsi_indicator = RSIIndicator(data['close'], window=self.period)
        # Calculate the RSI value using the RSIIndicator object and get the latest value
        rsi = rsi_indicator.rsi().iloc[-1]
        return rsi  # Return the latest RSI value
