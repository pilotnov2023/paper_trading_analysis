import pandas as pd

EXCHANGE_FEE_PERCENT = 0.08

# Replace 'positions.csv' with the actual path to your CSV file
file_path = 'positions.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path)

def calculate_long_close_price(position_open_price, long_profit):
    # Calculate close_price for a long position given long_profit and subtract exchange fee
    close_price = position_open_price * (1 + (long_profit + EXCHANGE_FEE_PERCENT) / 100)
    return close_price


def calculate_short_close_price(position_open_price, short_profit):
    # Calculate close_price for a short position given short_profit and subtract exchange fee
    close_price = position_open_price * (1 - (short_profit + EXCHANGE_FEE_PERCENT) / 100)
    return close_price

# Function to calculate lowest and highest prices based on runup and drawdown
def calculate_lowest_highest(position):
    position_open_price = float(position["position_open_price"])
    direction = position["direction"]
    current_position_runup = position["runup"]
    current_position_drawdown = position["drawdown"]

    if direction == "long":
        lowest_price = calculate_long_close_price(position_open_price , current_position_drawdown)
        highest_price = calculate_long_close_price(position_open_price , current_position_runup)
    else:  # Assuming short position
        lowest_price = calculate_short_close_price(position_open_price , current_position_runup)
        highest_price = calculate_short_close_price(position_open_price , current_position_drawdown)

    return lowest_price, highest_price

# Apply the function to each row of the DataFrame and assign the results to new columns
df[['lowest_price', 'highest_price']] = df.apply(calculate_lowest_highest, axis=1, result_type='expand')

# Create a copy of the DataFrame with reversed directions
df_reverse = df.copy()
df_reverse['rev_direction'] = df['direction'].apply(lambda x: 'long' if x == 'short' else 'short')

# Specify columns to be deleted
columns_to_delete = ['trailing_step', 'trailing_stop_price']

# Delete specified columns from the copy DataFrame
df_reverse = df_reverse.drop(columns=columns_to_delete)

# Save the reversed DataFrame to a new CSV file
reverse_file_path = 'reverse_positions.csv'
df_reverse.to_csv(reverse_file_path, index=False)

print(f"Reversed DataFrame saved to {reverse_file_path}")
