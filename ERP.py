import pandas as pd

import pandas as pd
# first comment
# Sample daily sales data
data = pd.DataFrame({
    'date': ['2024-11-10', '2024-11-11', '2024-11-12', '2024-11-13', '2024-11-14', '2024-11-15', '2024-11-16',
             '2024-11-10', '2024-11-11', '2024-11-12', '2024-11-13', '2024-11-14', '2024-11-15', '2024-11-16'],
    'product_id': [1, 1, 1, 1, 1, 1, 1,
                   2, 2, 2, 2, 2, 2, 2],
    'sales': [100, 150, 120, 80, 90, 70, 60,
              200, 180, 170, 160, 150, 140, 130]
})

# Convert date column to datetime
data['date'] = pd.to_datetime(data['date'])


# Group by product and week (using resample for weekly aggregation)
data.set_index('date', inplace=True)

# Calculate weekly sales for each product
weekly_sales = data.groupby('product_id').resample('W')['sales'].sum().reset_index()

print(weekly_sales)