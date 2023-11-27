import pandas as pd
import numpy as np

# Replace 'your_file.csv' with the actual path to your CSV file
file_path = 'positions.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Convert 'open_time' and 'close_time' to datetime objects
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])

# 1) Trading success rate
success_rate = (df['net_profit'] > 0).mean()
print(f"1) Trading Success Rate: {success_rate:.2%}")

# 2) Total profit and loss
total_profit_loss = df['net_profit'].sum()
print(f"2) Total Profit and Loss: {total_profit_loss:.2f}")

# 3) Average profit
average_profit = df[df['net_profit'] > 0]['net_profit'].mean()
print(f"3) Average Profit: {average_profit:.2f}")

# 4) Average loss
average_loss = df[df['net_profit'] < 0]['net_profit'].mean()
print(f"4) Average Loss: {average_loss:.2f}")

# 5) The biggest profit
biggest_profit = df['net_profit'].max()
print(f"5) Biggest Profit: {biggest_profit:.2f}")

# 6) The biggest loss
biggest_loss = df['net_profit'].min()
print(f"6) Biggest Loss: {biggest_loss:.2f}")

# 7) Total profits
total_profits = df[df['net_profit'] > 0]['net_profit'].sum()
print(f"7) Total Profits: {total_profits:.2f}")

# 8) Total losses
total_losses = df[df['net_profit'] < 0]['net_profit'].sum()
print(f"8) Total Losses: {total_losses:.2f}")

# 9) Total profit and loss by long, short transaction type
total_profit_long = df[df['direction'] == 'long']['net_profit'].sum()
total_profit_short = df[df['direction'] == 'short']['net_profit'].sum()
print(f"9) Total Profit and Loss by Long Transactions: {total_profit_long:.2f}")
print(f"   Total Profit and Loss by Short Transactions: {total_profit_short:.2f}")

# 10) Profit for long
profit_for_long = df[(df['direction'] == 'long') & (df['net_profit'] > 0)]['net_profit'].sum()
print(f"10) Profit for Long Positions: {profit_for_long:.2f}")

# 11) Loss for long
loss_for_long = df[(df['direction'] == 'long') & (df['net_profit'] < 0)]['net_profit'].sum()
print(f"11) Loss for Long Positions: {loss_for_long:.2f}")

# 12) Profit for short
profit_for_short = df[(df['direction'] == 'short') & (df['net_profit'] > 0)]['net_profit'].sum()
print(f"12) Profit for Short Positions: {profit_for_short:.2f}")

# 13) Loss for short
loss_for_short = df[(df['direction'] == 'short') & (df['net_profit'] < 0)]['net_profit'].sum()
print(f"11) Loss for Short Positions: {loss_for_short:.2f}")


# Calculate the potential profit and potential loss for each trade
# Calculate potential profit and potential loss
df['potential_profit'] = df['net_profit'].apply(lambda x: max(x, 0))
df['potential_loss'] = df['net_profit'].apply(lambda x: min(x, 0))

# Calculate the total potential profit and total potential loss
total_potential_profit = df['potential_profit'].sum()
total_potential_loss = df['potential_loss'].sum()

# Calculate the overall risk/reward ratio
overall_risk_reward_ratio = -total_potential_profit / total_potential_loss

# Display the overall risk/reward ratio
print(f"12) Overall Risk/Reward Ratio: {overall_risk_reward_ratio:.2f}")