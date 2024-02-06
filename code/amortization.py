# %%
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import matplotlib.pyplot as plt

def create_amortization_table_corrected(house_value, annual_interest_rate, loan_term_years, down_payment, start_date, extra_payment):
    initial_balance = house_value - down_payment
    monthly_interest_rate = (annual_interest_rate / 100) / 12
    total_payments = loan_term_years * 12
    monthly_payment = initial_balance * (monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** (-total_payments)))
    remaining_balance = initial_balance
    total_paid = 0
    
    dates, months, payments, principals, interests, balances, extra_payments, total_paids = [], [], [], [], [], [], [], []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    
    for month in range(1, total_payments + 1):
        if remaining_balance <= 0:
            break  # Stop if loan is already paid off
        
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        actual_extra_payment = extra_payment if remaining_balance - principal_payment > extra_payment else remaining_balance - principal_payment
        
        total_payment = principal_payment + interest_payment + actual_extra_payment
        remaining_balance -= (principal_payment + actual_extra_payment)
        
        dates.append(current_date.strftime("%Y-%m-%d"))
        months.append(month)
        payments.append(round(total_payment, 2))
        principals.append(round(principal_payment, 2))
        interests.append(round(interest_payment, 2))
        balances.append(round(remaining_balance, 2))
        extra_payments.append(round(actual_extra_payment, 2))
        total_paids.append(round(total_paid + total_payment, 2))
        total_paid += total_payment
        
        current_date += relativedelta(months=+1)
    
    amortization_df_corrected = pd.DataFrame({
        'Date': dates,
        'Month': months,
        'Payment': payments,
        'Principal': principals,
        'Interest': interests,
        'Extra Payment': extra_payments,
        'Remaining Balance': balances,
        'Total Paid': total_paids
    })
    
    return amortization_df_corrected

# use
house_value = 250000
annual_interest_rate = 7.75
loan_term_years = 15
down_payment = 130000
start_date = "2024-01-01" 
extra_payment = 300

amortization_df = create_amortization_table_corrected(house_value, annual_interest_rate, loan_term_years, down_payment, start_date, extra_payment)

print(amortization_df['Payment'][0])
amortization_df.head()
amortization_df.to_csv('./../data/amortization.csv', index=False)

# %%

loan_data = amortization_df

# Preprocessing and calculations
loan_data['Date'] = pd.to_datetime(loan_data['Date'])
loan_data['Months Since Start'] = (loan_data['Date'].dt.year - loan_data['Date'].dt.year.min()) * 12 + loan_data['Date'].dt.month - loan_data['Date'].dt.month.min()
loan_data['Cumulative Principal'] = loan_data['Principal'].cumsum() + loan_data['Extra Payment'].cumsum()
loan_data['Cumulative Interest'] = loan_data['Interest'].cumsum()
total_paid = loan_data['Payment'].sum() + loan_data['Extra Payment'].sum()
total_interest_paid = loan_data['Cumulative Interest'].iloc[-1]
total_principal_paid = loan_data['Cumulative Principal'].iloc[-1]
total_months_to_pay_off = loan_data['Month'].max()
# Determine the maximum value for the y-axis limit based on the cumulative principal
max_y_value = loan_data['Cumulative Principal'].max()


# Creating the chart
fig, ax = plt.subplots(figsize=(12, 8))

# Plot Remaining Balance
ax.plot(loan_data['Months Since Start'], loan_data['Remaining Balance'], color='black', label='Remaining Balance')

# Plot Cumulative Principal with shading
ax.fill_between(loan_data['Months Since Start'], 0, loan_data['Cumulative Principal'], color='green', alpha=0.3, label='Cumulative Principal')
ax.plot(loan_data['Months Since Start'], loan_data['Cumulative Principal'], color='green')

# Plot Cumulative Interest with shading
ax.fill_between(loan_data['Months Since Start'], 0, loan_data['Cumulative Interest'], color='red', alpha=0.3, label='Cumulative Interest')
ax.plot(loan_data['Months Since Start'], loan_data['Cumulative Interest'], color='red')

# Set labels and title
ax.set_xlabel('Months Since Start')
ax.set_ylabel('Amount ($)')
plt.title('Loan Amortization Schedule', size=20)

# Remove gridlines
ax.grid(False)

# Adjust x-ticks to show every month
ax.set_xticks(loan_data['Months Since Start'])
ax.set_xticklabels(loan_data['Months Since Start'], rotation=45)

# Adding a legend
ax.legend()

# Adding text annotation
text_str = f"Total Amount Paid: ${total_paid:,.2f}\nTotal Paid to Interest: ${total_interest_paid:,.2f}\nTotal Paid to Principal: ${total_principal_paid:,.2f}\nTotal Months to Pay Off: {total_months_to_pay_off}"
ax.text(0.5, 0.98, text_str, transform=ax.transAxes, fontsize=12, verticalalignment='top', horizontalalignment='center')

plt.tight_layout()
plt.show()


# %%
