#%%
import matplotlib.pyplot as plt
import numpy as np

# Data
interest_rates = [6.25, 6.125, 6.00, 5.875, 5.75, 5.625, 5.5, 5.375, 5.25, 5.125, 5.00, 4.875]
apr_values = [6.419, 6.13, 6.227, 6.141, 6.075, 5.988, 5.921, 5.834, 5.768, 5.720, 5.653, 5.606]
payments = [1834, 1820, 1805, 1791, 1777, 1762, 1748, 1734, 1720, 1705, 1692, 1678]
points = [0, 0.125, 0.375, 0.625, 1.00, 1.25, 1.625, 1.875, 2.25, 2.75, 3.125, 3.625]
costs = [0, 267, 802, 1337, 2140, 2675, 3477, 4012, 4815, 5885, 6687, 7757]

# Create the figure
fig, ax1 = plt.subplots()

# Plot points vs. costs
ax1.plot(points, costs, 'ro-', label='Cost (USD)')
ax1.set_xlabel('Points')
ax1.set_ylabel('Cost (USD)')
ax1.legend(loc='upper left')

# Create a second y-axis for the interest rates and APR values
ax2 = ax1.twinx()
ax2.plot(points, interest_rates, 'bs-', label='Interest Rate (%)')
ax2.plot(points, apr_values, 'gs-', label='APR (%)')
ax2.set_ylabel('Interest Rate / APR (%)')
ax2.legend(loc='upper right')

# Add a third y-axis for payments
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))
ax3.plot(points, payments, 'mo-', label='Monthly Payment (USD)')
ax3.set_ylabel('Monthly Payment (USD)')
ax3.legend(loc='lower right')

plt.title("Mortgage Analysis: Costs, Interest Rates, APR, and Payments vs. Points")
plt.show()

# %%
import numpy as np

# House and loan parameters
house_cost = 350000
down_payment = 130000
loan_amount = house_cost - down_payment
months_to_pay = 6 * 12  # 5 years in months

# Data
interest_rates = [6.25, 6.125, 6.00, 5.875, 5.75, 5.625, 5.5, 5.375, 5.25, 5.125, 5.00, 4.875]
payments = [1834, 1820, 1805, 1791, 1777, 1762, 1748, 1734, 1720, 1705, 1692, 1678]
points = [0, 0.125, 0.375, 0.625, 1.00, 1.25, 1.625, 1.875, 2.25, 2.75, 3.125, 3.625]
costs = [0, 267, 802, 1337, 2140, 2675, 3477, 4012, 4815, 5885, 6687, 7757]

# Function to calculate the total cost over 5 years, including the points cost
def calculate_total_cost(payment, points_cost):
    total_monthly_cost = payment * months_to_pay
    return total_monthly_cost + points_cost

# Iterate through each rate option and calculate the total cost over 5 years
total_costs = [calculate_total_cost(payment, cost) for payment, cost in zip(payments, costs)]

# Find the index of the minimum total cost
optimal_index = np.argmin(total_costs)

# Retrieve the optimal interest rate, points, and associated cost
optimal_interest_rate = interest_rates[optimal_index]
optimal_points = points[optimal_index]
optimal_cost = total_costs[optimal_index]

# Display the optimal option
print(f"The optimal amount to buy down the interest rate is {optimal_points} points.")
print(f"This will give an interest rate of {optimal_interest_rate}%, with a total cost over 5 years of ${optimal_cost:.2f}.")
