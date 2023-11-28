import pandas as pd
from tabulate import tabulate

EXCHANGE_FEE_PERCENT = 0.08
TAKE_PROFIT_PERCENT = 0.04
STOP_LOSS_PERCENT = -0.02

# Replace 'positions.csv' with the actual path to your CSV file
file_path = 'positions.csv'

# Load the CSV file into a DataFrame
original_df = pd.read_csv(file_path)

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
original_df[['lowest_price', 'highest_price']] = original_df.apply(calculate_lowest_highest, axis=1, result_type='expand')

# Create a copy of the DataFrame with reversed directions
df_reverse = original_df.copy()
df_reverse['rev_direction'] = original_df['direction'].apply(lambda x: 'long' if x == 'short' else 'short')

# Specify columns to be deleted
columns_to_delete = ['trailing_step', 'trailing_stop_price']

# Delete specified columns from the copy DataFrame
df_reverse = df_reverse.drop(columns=columns_to_delete)

# Function to calculate rev_net_profit based on conditions
def calculate_rev_net_profit(row):
    position_open_price = row['position_open_price']
    direction = row['rev_direction']
    
    if direction == 'long':
        close_price_take_profit = row['highest_price']
        close_price_stop_loss = row['lowest_price']
        
        profit_take_profit = round(
            ((close_price_take_profit - position_open_price) / position_open_price) * 100 - EXCHANGE_FEE_PERCENT, 2
        )
        profit_stop_loss = round(
            ((close_price_stop_loss - position_open_price) / position_open_price) * 100 - EXCHANGE_FEE_PERCENT, 2
        )
        
        if profit_take_profit >= TAKE_PROFIT_PERCENT:
            return TAKE_PROFIT_PERCENT # profit_take_profit
        elif profit_stop_loss <= STOP_LOSS_PERCENT:
            return STOP_LOSS_PERCENT # profit_stop_loss
        else:
            return None
        
    elif direction == 'short':
        close_price_take_profit = row['lowest_price']
        close_price_stop_loss = row['highest_price']
        
        profit_take_profit = round(
            ((position_open_price - close_price_take_profit) / position_open_price) * 100 - EXCHANGE_FEE_PERCENT, 2
        )
        profit_stop_loss = round(
            ((position_open_price - close_price_stop_loss) / position_open_price) * 100 - EXCHANGE_FEE_PERCENT, 2
        )
        
        if profit_take_profit >= TAKE_PROFIT_PERCENT:
            return TAKE_PROFIT_PERCENT # profit_take_profit
        elif profit_stop_loss <= STOP_LOSS_PERCENT:
            return STOP_LOSS_PERCENT # profit_stop_loss
        else:
            return None

# Apply the function to each row of the DataFrame and assign the results to the new column
# Apply the function to each row of the DataFrame and assign the results to the new column
df_reverse['rev_net_profit'] = df_reverse.apply(calculate_rev_net_profit, axis=1)

# Save the reversed DataFrame to a new CSV file
reverse_file_path = 'reverse_positions.csv'
df_reverse.to_csv(reverse_file_path, index=False)

print(f"Reversed DataFrame saved to {reverse_file_path}")

df = df_reverse.copy()

# 0) Calculate the count of all positions
total_positions = df.shape[0]

# 1) Trading success rate
success_rate = (df['rev_net_profit'] > 0).mean()

# 2) Total profit and loss
total_profit_loss = df['rev_net_profit'].sum()

# 3) Average profit
average_profit = df[df['rev_net_profit'] > 0]['rev_net_profit'].mean()

# 4) Average loss
average_loss = df[df['rev_net_profit'] < 0]['rev_net_profit'].mean()

# 5) The biggest profit
biggest_profit = df['rev_net_profit'].max()

# 6) The biggest loss
biggest_loss = df['rev_net_profit'].min()

# 7) Total profits
total_profits = df[df['rev_net_profit'] > 0]['rev_net_profit'].sum()

# 8) Total losses
total_losses = df[df['rev_net_profit'] < 0]['rev_net_profit'].sum()

# 9) Total profit and loss by long, short transaction type
total_profit_long = df[df['rev_direction'] == 'long']['rev_net_profit'].sum()
total_profit_short = df[df['rev_direction'] == 'short']['rev_net_profit'].sum()

# 10) Profit for long
profit_for_long = df[(df['rev_direction'] == 'long') & (
    df['rev_net_profit'] > 0)]['rev_net_profit'].sum()

# 11) Loss for long
loss_for_long = df[(df['rev_direction'] == 'long') & (
    df['rev_net_profit'] < 0)]['rev_net_profit'].sum()

# 12) Profit for short
profit_for_short = df[(df['rev_direction'] == 'short') & (
    df['rev_net_profit'] > 0)]['rev_net_profit'].sum()

# 13) Loss for short
loss_for_short = df[(df['rev_direction'] == 'short') & (
    df['rev_net_profit'] < 0)]['rev_net_profit'].sum()

# Calculate the potential profit and potential loss for each trade
# Calculate potential profit and potential loss
df['potential_profit'] = df['rev_net_profit'].apply(lambda x: max(x, 0))
df['potential_loss'] = df['rev_net_profit'].apply(lambda x: min(x, 0))

# Calculate the total potential profit and total potential loss
total_potential_profit = df['potential_profit'].sum()
total_potential_loss = df['potential_loss'].sum()

# Calculate the overall risk/reward ratio
overall_risk_reward_ratio = -total_potential_profit / total_potential_loss

# Display results in tabular format
results_table = [
    ["0", "Number Of Trades", total_positions],
    ["1", "Trading Success Rate", f"{success_rate:.2%}"],
    ["2", "Total Profit and Loss", f"{total_profit_loss:.2f}"],
    ["3", "Average Profit", f"{average_profit:.2f}"],
    ["4", "Average Loss", f"{average_loss:.2f}"],
    ["5", "Biggest Profit", f"{biggest_profit:.2f}"],
    ["6", "Biggest Loss", f"{biggest_loss:.2f}"],
    ["7", "Total Profits", f"{total_profits:.2f}"],
    ["8", "Total Losses", f"{total_losses:.2f}"],
    ["9", "Total Profit and Loss by Long Transactions",f"{total_profit_long:.2f}", f"{total_profit_short:.2f}"],
    ["10", "Profit for Long Positions", f"{profit_for_long:.2f}"],
    ["11", "Loss for Long Positions", f"{loss_for_long:.2f}"],
    ["12", "Profit for Short Positions", f"{profit_for_short:.2f}"],
    ["13", "Loss for Short Positions", f"{loss_for_short:.2f}"],
    ["14", "Overall Risk/Reward Ratio", f"{overall_risk_reward_ratio:.2f}"]
]

print(tabulate(results_table, headers=["Row","Metric", "Value"], tablefmt="pretty", colalign=("center", "center")))

