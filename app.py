import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Comprehensive Retirement Planner", layout="wide")
st.title("Comprehensive Retirement Planner")
st.subheader("Integrate income, expenses, debt, and investments to estimate your retirement savings.")

# ------------------------------------------------
# Income and Promo
# ------------------------------------------------
st.header("Income & Promotion")

def calculate_tax(annual_salary):
    """Return the total federal tax based on the 2023 brackets."""
    tax_brackets = [
        (0, 11925, 0.10),
        (11925, 48475, 0.12),
        (48475, 103350, 0.22),
        (103350, 197300, 0.24),
        (197300, 250525, 0.32),
        (250525, 539900, 0.35),
        (539900, float('inf'), 0.37)
    ]
    total_tax = 0
    for lower, upper, rate in tax_brackets:
        if annual_salary > lower:
            taxable = min(annual_salary, upper) - lower
            total_tax += taxable * rate
        else:
            break
    return total_tax

annual_salary = st.number_input("Enter your salary:", min_value=0.0, value=60000.0, step=1.0)

promotion_frequency = st.slider("Promotion every X years:", min_value=1, max_value=10, value=5, step=1)
raise_percent = st.slider("Raise percentage at promotion (%):", min_value=0.0, max_value=20.0, value=5.0, step=0.5) / 100

def get_effective_tax_rate(salary):
    tax_bill = calculate_tax(salary)
    return tax_bill / salary if salary > 0 else 0

current_tax_bill = calculate_tax(annual_salary)
ef_tax = get_effective_tax_rate(annual_salary)
if annual_salary > 0:
    st.write(f"Your total tax bill is: ${current_tax_bill:,.2f}")
    st.write(f"Your effective tax rate is: {ef_tax:.2%}")


# ------------------------------------------------
# Expenses
# ------------------------------------------------
st.header("Monthly Expenses")

import streamlit as st
import plotly.express as px

st.subheader("Living Expenses")

rent = st.number_input("Rent / Mortgage ($):", min_value=0.0, step=50.0, value=1000.0)
utilities = st.number_input("Utilities (Electric, Water, etc.) ($):", min_value=0.0, step=10.0, value=150.0)
food = st.number_input("Food / Groceries ($):", min_value=0.0, step=10.0, value=400.0)
transportation = st.number_input('Transportation ($):', min_value=0.0, step=10.0, value=200.0)
total_insurance=st.number_input('Total Insurance Payments ($):', min_value=0.0, step=10.0, value=200.0)
other_living_expenses =st.number_input('Other Living Expenses ($):', min_value=0.0, step=10.0, value=200.00)

st.subheader("Discretionary Expenses")
entertainment = st.number_input("Entertainment ($):", min_value=0.0, step=10.0, value=200.0)
travel = st.number_input("Travel ($):", min_value=0.0, step=10.0, value=300.0)
other_discretionary_expenses = st.number_input('Other Discretionary ($):', min_value=0.0, step=10.0, value=775.00)

monthly_expenses = rent + utilities + food + transportation + total_insurance + other_living_expenses + entertainment + travel + other_discretionary_expenses
monthly_income = (annual_salary - current_tax_bill) / 12

st.write(f"**Total Monthly Expenses:** ${monthly_expenses:,.2f}")

necessities_total = rent + utilities + food + transportation + total_insurance + other_living_expenses
discretionary_total = travel + entertainment + other_discretionary_expenses
savings = monthly_income - necessities_total - discretionary_total

necessities_percentage = (necessities_total / monthly_income) * 100
discretionary_percentage = (discretionary_total / monthly_income) * 100
savings_percentage = (savings / monthly_income) * 100

if necessities_percentage > 50:
    st.warning("**Warning:** Your basic living expenses (needs) are above 50% of your monthly income! The recomended budget sugests keeping your total amount spent on needs at or below 50% ")
if discretionary_percentage > 30:
    st.warning("**Warning:** Your discretionary expenses (wants) are above 30% of your monthly income! The recomended budget sugests keeping your total amount spent on wants at or below 30% ")

categories = ['Necessities', 'Discretionary', 'Savings']
values = [necessities_total, discretionary_total, savings]

st.markdown("**Monthly Paycheck Utilization**: Using the standard budgeting rule 50% Necessities / 30% Discretionary / 20% Savings")
st.markdown("**Note**: Net income not spent will be considered part of your savingsd)
fig = px.pie(names=categories, values=values)

st.plotly_chart(fig)

st.subheader("Debt Repayment")
debt_principal = st.number_input("Outstanding Debt Principal ($):", min_value=0.0, step=500.0, value=5_000.0)
debt_annual_interest = st.slider("Debt Annual Interest Rate (%):", min_value=0.0, max_value=30.0, value=5.0, step=0.5) / 100
debt_monthly_payment = st.number_input("Monthly Debt Payment ($):", min_value=0.0, step=50.0, value=200.0)

# ------------------------------------------------
# Emergency
# ------------------------------------------------
st.header("Emergency Fund")

months_of_emergency_fund = st.slider(
    "How many months of expenses should your emergency fund cover?",
    min_value=1, max_value=36, value=6
)
total_emergency_fund = months_of_emergency_fund * monthly_expenses

st.write(f"To cover {months_of_emergency_fund} months of expenses, "
         f"you need an emergency fund of: **${total_emergency_fund:,.2f}**")

# ------------------------------------------------
# Investments
# ------------------------------------------------
st.header("Investments")

current_savings = st.number_input("Current Savings ($) :", min_value=0.0, step=1000.0, value=10_000.0)
portfolio_value = st.number_input("Current Portfolio Value ($) :", min_value=0.0, step=1000.0, value=10_000.0)

stock_allocation = st.slider("Stock Allocation (%):", min_value=0.0, max_value=100.0, value=70.0, step=1.0) / 100
mutual_fund_allocation = st.slider("Mutual Fund Allocation (%):", min_value=0.0, max_value=100.0, value=10.0, step=1.0) / 100
bond_allocation = st.slider("Bond Allocation (%):", min_value=0.0, max_value=100.0, value=20.0, step=1.0) / 100
other_allocation = 1.0 - (stock_allocation + mutual_fund_allocation + bond_allocation)

stock_annual_return = st.number_input("Expected Annual Return (Stocks) (%):", min_value=0.0, step=0.5, value=8.0)
mutual_fund_annual_return = st.number_input("Expected Annual Return (Mutual Funds) (%):", min_value=0.0, step=0.5, value=6.0)
bond_annual_return = st.number_input("Expected Annual Return (Bonds) (%):", min_value=0.0, step=0.5, value=5.0)
other_annual_return = st.number_input("Expected Annual Return (Other) (%):", min_value=0.0, step=0.5, value=4.0)
savings_annual_return = st.number_input("Expected Annual Return (Savings) (%):", min_value=0.0, step=0.01, value=0.42)

monthly_portfolio_contribution = st.number_input("Additional Monthly Contribution to Portfolio ($) :",
                                                 min_value=0.0, step=50.0, value=100.0)

years_to_retirement = st.slider("Years until retirement:", min_value=1, max_value=50, value=30, step=1)

total_allocation = stock_allocation + mutual_fund_allocation + bond_allocation + other_allocation

if total_allocation > 1:
    st.error("Overallocated: your allocations exceed 100%. Please adjust.")

# Check & Notify About Emergency Fund
if current_savings >= total_emergency_fund:
    st.success("You have enough savings to cover your emergency fund!")
else:
    needed = total_emergency_fund - current_savings
    st.warning(f"You need **${needed:,.2f}** more to fully fund your emergency reserve.")

# ------------------------------------------------
# Simulation
# ------------------------------------------------
st.header("Retirement Simulation")

st.write("""
Click the **"Run Simulation"** button to calculate the monthly evolution of each asset class
(Stocks, Mutual Funds, Bonds, Other, and your separate Savings) until retirement.
We assume monthly returns are simply (annual_return / 12).
Salary promotions happen on the specified frequency, which affects your net monthly pay
and thus your monthly investment contributions.
""")

run_simulation = st.button("Run Simulation")

if run_simulation:
    # ---  Initialize Values ---
    total_months = years_to_retirement * 12

    # Break down current portfolio
    stock_value = portfolio_value * stock_allocation
    mf_value = portfolio_value * mutual_fund_allocation
    bond_value = portfolio_value * bond_allocation
    other_value = portfolio_value * other_allocation

    # Current savings is separate from the 'portfolio'
    saving_value = current_savings

    # Track monthly data for plotting
    months_index = np.arange(total_months + 1)  # 0 ... total_months
    years_axis = months_index / 12.0           # Convert months to years for the x-axis

    stock_history = [stock_value]
    mf_history = [mf_value]
    bond_history = [bond_value]
    other_history = [other_value]
    saving_history = [saving_value]

    # Starting annual salary & monthly net
    cur_annual_salary = annual_salary
    cur_tax_rate = ef_tax  # from the initial calculation
    monthly_net_income = (cur_annual_salary * (1 - cur_tax_rate)) / 12

    # --- Simulation Loop ---
    for m in range(1, total_months + 1):
        # Every 12 months, check for promotion
        if m % 12 == 0:
            years_passed = m // 12
            # Check if this year is a promotion year
            if years_passed % promotion_frequency == 0:
                # Apply raise
                cur_annual_salary *= (1 + raise_percent)
                # Recalculate tax for new salary
                new_tax_bill = calculate_tax(cur_annual_salary)
                cur_tax_rate = new_tax_bill / cur_annual_salary if cur_annual_salary > 0 else 0

            # Update monthly net after adjusting salary/tax
            monthly_net_income = (cur_annual_salary * (1 - cur_tax_rate)) / 12

        # --- Debt Payment ---
        monthly_debt_interest = (debt_annual_interest / 12) * debt_principal
        debt_principal = debt_principal + monthly_debt_interest - debt_monthly_payment
        if debt_principal < 0:
            debt_principal = 0

        # --- Determine how much can go into investments each month ---
        leftover_for_investments = monthly_net_income - monthly_expenses - debt_monthly_payment
        if leftover_for_investments < 0:
            leftover_for_investments = 0  # No negative investments

        # Add user-defined additional monthly contribution
        total_portfolio_contribution = leftover_for_investments + monthly_portfolio_contribution

        # Split the contribution across different asset classes
        cont_stocks = total_portfolio_contribution * stock_allocation
        cont_mf = total_portfolio_contribution * mutual_fund_allocation
        cont_bond = total_portfolio_contribution * bond_allocation
        cont_other = total_portfolio_contribution * other_allocation

        # --- Update each asset with monthly return + monthly contribution ---
        stock_value = stock_value * (1 + (stock_annual_return/100)/12) + cont_stocks
        mf_value    = mf_value    * (1 + (mutual_fund_annual_return/100)/12) + cont_mf
        bond_value  = bond_value  * (1 + (bond_annual_return/100)/12) + cont_bond
        other_value = other_value * (1 + (other_annual_return/100)/12) + cont_other

        # --- Update separate Savings with monthly return ---
        saving_value = saving_value * (1 + (savings_annual_return/100)/12)

        # --- Store for plotting ---
        stock_history.append(stock_value)
        mf_history.append(mf_value)
        bond_history.append(bond_value)
        other_history.append(other_value)
        saving_history.append(saving_value)

    # --- Plotly Figure ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years_axis, y=stock_history,
                             mode='lines', name='Stocks'))
    fig.add_trace(go.Scatter(x=years_axis, y=mf_history,
                             mode='lines', name='Mutual Funds'))
    fig.add_trace(go.Scatter(x=years_axis, y=bond_history,
                             mode='lines', name='Bonds'))
    fig.add_trace(go.Scatter(x=years_axis, y=other_history,
                             mode='lines', name='Other'))
    fig.add_trace(go.Scatter(x=years_axis, y=saving_history,
                             mode='lines', name='Savings'))

    fig.update_layout(
        title="Asset Values Over Time",
        xaxis_title="Years",
        yaxis_title="Value (in $)",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Show final amounts
    st.write(f"**Final Stock Value:** ${stock_value:,.2f}")
    st.write(f"**Final Mutual Fund Value:** ${mf_value:,.2f}")
    st.write(f"**Final Bond Value:** ${bond_value:,.2f}")
    st.write(f"**Final Other Value:** ${other_value:,.2f}")
    st.write(f"**Final Savings Value:** ${saving_value:,.2f}")
    st.write(
        f"**Remaining Debt Principal:** ${debt_principal:,.2f}"
        if debt_principal > 0
        else "Your debt has been fully repaid!"
    )

 # Pie chart of expenses (monthly average)
st.subheader("Monthly Expense Breakdown")

avg_rent = rent
avg_utilities = utilities
avg_food = food
avg_transportation = transportation
avg_total_insurance = total_insurance
avg_other_living_expenses = other_living_expenses
avg_entertainment = entertainment
avg_travel = travel
avg_other_discretionary_expenses = other_discretionary_expenses
avg_portfolio_contribution = monthly_portfolio_contribution

labels = ["Rent/Mortgage", "Utilities", "Food", "Transportation", "Total Insurance Payments", "Other Living Expenses", "Entertainment", "Travel", "Other Discretionary Expenses", "Debt Payment", "Portfolio Contribution"]
values = [
    avg_rent,
    avg_utilities,
    avg_food,
    avg_transportation,
    avg_total_insurance,
    avg_other_living_expenses,
    avg_entertainment,
    avg_travel,
    avg_other_discretionary_expenses,
    debt_monthly_payment,
    avg_portfolio_contribution,
]

fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
fig_pie.update_layout(title="Average Monthly Expense Breakdown")
st.plotly_chart(fig_pie, use_container_width=True)

st.write("---")
st.write("### Summary of Key Inputs")
col1, col2 = st.columns(2)
with col1:
    st.write(f"**Initial Annual Salary:** ${annual_salary:,.2f}")
    st.write(f"**Effective Tax Rate:** {ef_tax*100:.2f}%")
    st.write(f"**Promotion Frequency:** Every {promotion_frequency} years")
    st.write(f"**Raise Percentage:** {raise_percent*100:.1f}%")
with col2:
    st.write(f"**Debt Principal:** ${debt_principal:,.2f}")
    st.write(f"**Debt Interest Rate:** {debt_annual_interest*100:.2f}%")
    st.write(f"**Debt Monthly Payment:** ${debt_monthly_payment:,.2f}")
    st.write(f"**Current Savings:** ${current_savings:,.2f}")

st.write("---")
st.markdown("""
**Instructions**
1. Adjust the inputs above to see how they affect your retirement outlook.
2. Experiment with different promotion frequencies, debt payments, and investment allocations.
3. Aim to pay off debt and grow your investments for better retirement outcomes.
""")
