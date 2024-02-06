#%%
import matplotlib.pyplot as plt
import pandas as pd
downpayment = 130000
df = pd.read_csv('./../data/amortization.csv')
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
    text_str = f"${loan+130000:,.0f} total = ${downpayment:,} down + ${loan:,.0f} loan\n\${loan_data['Extra Payment'][0] + loan_data['Principal'][0] + loan_data['Interest'][0]:,.0f} monthly =  ${loan_data['Principal'][0] + loan_data['Interest'][0]:,.0f} required + \${loan_data['Extra Payment'][0]:,.0f} extra\nYou paid ${loan_data['Total Paid'].iloc[-1]:,.0f} after loan+interest\nTotal interest paid: ${loan_data['Interest'].sum():,.0f}\nMonths to pay off:{loan_data['Month'].iloc[-1]}"
    ax.text(0.35, 0.98, text_str, transform=ax.transAxes, fontsize=13, verticalalignment='top', horizontalalignment='left')

    plt.tight_layout()
    # plt.savefig(f'./../figs/home{loan+130000:,.0f}-pay{t_payment}.png', bbox_inches='tight', dpi=300)
    plt.show()
    plt.close()

create_loan_amortization_chart(df, downpayment)
# %%
