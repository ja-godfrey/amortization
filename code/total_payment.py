# %%
# this is the same as amortization, but you say how much you can afford to pay per month and then it adds the remainder onto your extra automatically
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

def create_amortization_table(house_value, annual_interest_rate, loan_term_years, down_payment, start_date, total_payment):
    initial_balance = house_value - down_payment
    monthly_interest_rate = (annual_interest_rate / 100) / 12
    total_payments = loan_term_years * 12
    monthly_payment = initial_balance * (monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** (-total_payments)))
    remaining_balance = initial_balance
    extra_payment = total_payment - monthly_payment
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
house_value = 225000
annual_interest_rate = 7.75
loan_term_years = 15
down_payment = 130000
start_date = "2024-01-01" 
total_payment = 4000

amortization_df = create_amortization_table(house_value, annual_interest_rate, loan_term_years, down_payment, start_date, total_payment)

print(f'required monthly payment: {amortization_df["Principal"][0] + amortization_df["Interest"][0]}')
amortization_df.head()
amortization_df.to_csv('./../data/amortization.csv', index=False)
# create_loan_amortization_chart(amortization_df, down_payment=down_payment)

