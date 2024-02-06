# %%
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

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

def create_loan_amortization_chart(loan_data, down_payment=0):
    # Calculate the loan amount by summing the Principal and Extra Payments
    loan = round(loan_data['Principal'].sum() + loan_data['Extra Payment'].sum())

    # Calculating Cumulative Principal and Interest Paid
    loan_data['Cumulative Principal'] = loan_data['Principal'].cumsum()
    loan_data['Cumulative Interest'] = loan_data['Interest'].cumsum()

    # Create a figure and a set of subplots
    fig, ax = plt.subplots(figsize=(14, 8))

    # Plot the data
    ax.plot(loan_data['Month'], loan_data['Remaining Balance'], label='Remaining Balance', color='black')
    ax.plot(loan_data['Month'], loan_data['Cumulative Principal'], label='Cumulative Principal Paid', color='green')
    ax.plot(loan_data['Month'], loan_data['Cumulative Interest'], label='Cumulative Interest Paid', color='red')
    ax.plot(loan_data['Month'], loan_data['Total Paid'], label='Total Paid', color='blue')

    ax.fill_between(loan_data['Month'], loan_data['Cumulative Principal'], color='green', alpha=0.1)
    ax.fill_between(loan_data['Month'], loan_data['Total Paid'], color='blue', alpha=0.1)
    ax.fill_between(loan_data['Month'], loan_data['Cumulative Interest'], color='red', alpha=0.1)

    # Set title and labels
    ax.set_title('Loan Amortization Schedule', size=20)
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount ($)')

    # Format the x-axis
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Set limits
    ax.set_xlim(left=1, right=loan_data['Month'].iloc[-1])
    ax.set_ylim(bottom=0, top=loan_data['Total Paid'].iloc[-1])

    # Rotate x-ticks, set legend, grid and layout
    plt.xticks(rotation=45)
    ax.legend()
    ax.grid(False)
    plt.tight_layout()

    # Add text annotation
    text_str = f"${loan+130000:,.0f} total = ${down_payment:,} down + ${loan:,.0f} loan\n\${loan_data['Extra Payment'][0] + loan_data['Principal'][0] + loan_data['Interest'][0]:,.0f} monthly =  ${loan_data['Principal'][0] + loan_data['Interest'][0]:,.0f} required + \${loan_data['Extra Payment'][0]:,.0f} extra\nYou paid ${loan_data['Total Paid'].iloc[-1]:,.0f} after loan+interest\nTotal interest paid: ${loan_data['Interest'].sum():,.0f}\nMonths to pay off:{loan_data['Month'].iloc[-1]}"
    ax.text(0.35, 0.98, text_str, transform=ax.transAxes, fontsize=13, verticalalignment='top', horizontalalignment='left')

    plt.tight_layout()
    plt.savefig(f'./../figs/home{loan+130000:,.0f}-pay{t_payment}.png', bbox_inches='tight', dpi=300)
    plt.show()
    plt.close()

annual_interest_rate = 7.75
loan_term_years = 30
down_payment = 130000
start_date = "2024-01-01" 

t_payments = [3000, 4000, 4500]
h_values = [180000, 225000, 250000]

for h_value in h_values:
    for t_payment in t_payments:
        loan_data = create_amortization_table(h_value, annual_interest_rate, loan_term_years, down_payment, start_date, t_payment)
        create_loan_amortization_chart(loan_data, down_payment=down_payment)

# %%
