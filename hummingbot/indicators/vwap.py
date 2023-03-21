# Import the pandas library for data manipulation
import pandas as pd

# Create a VWAPIndicator class
class VWAPIndicator:
    # Initialize the class
    def __init__(self):
        # Create an empty DataFrame with columns for high, low, close, and volume
        self.data = pd.DataFrame(columns=['high', 'low', 'close', 'volume'])

    # Define a method to update the DataFrame with new data
    def update(self, high, low, close, volume):
        # Create a dictionary containing the new data
        new_data = {'high': high, 'low': low, 'close': close, 'volume': volume}
        # Append the new data to the DataFrame, ignoring the index
        self.data = self.data.append(new_data, ignore_index=True)

    # Define a method to calculate the VWAP
    def calculate(self):
        # Calculate the typical price for each row in the DataFrame
        self.data['typical_price'] = (self.data['high'] + self.data['low'] + self.data['close']) / 3
        # Calculate the typical price multiplied by the volume for each row in the DataFrame
        self.data['tpv'] = self.data['typical_price'] * self.data['volume']
        # Calculate the cumulative TPV (typical price * volume) by summing the 'tpv' column
        cumulative_tpv = self.data['tpv'].sum()
        # Calculate the cumulative volume by summing the 'volume' column
        cumulative_volume = self.data['volume'].sum()
        # Calculate and return the VWAP by dividing the cumulative TPV by the cumulative volume
        return cumulative_tpv / cumulative_volume
