import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

st.set_page_config(
    page_title="Customer Churn Dashboard",
    page_icon="📉",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv(r"C:\Users\ACER\churn\telco_churn_clean.csv")

@st.cache_resource
def load_model():
    return joblib.load(r"C:\Users\ACER\churn\churn_model.pkl")

df = load_data()
model = load_model()

st.sidebar.title("📉 Churn Analysis")
st.sidebar.markdown("Telco Customer Churn Project")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Customer Segments", "Churn Predictor"]
)

if page == "Overview":

    st.title("Customer Churn Dashboard")
    st.markdown("##### Telco dataset · 7,032 customers · Random Forest model (AUC 0.838)")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    total = len(df)
    churned = df['Churn'].sum()
    churn_rate = churned / total * 100
    avg_monthly = df[df['Churn']==1]['MonthlyCharges'].mean()

    col1.metric("Total Customers", f"{total:,}")
    col2.metric("Churned Customers", f"{int(churned):,}")
    col3.metric("Churn Rate", f"{churn_rate:.1f}%")
    col4.metric("Avg Monthly Charge (churned)", f"${avg_monthly:.0f}")

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Avg monthly charges by churn status")
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        churn_contract = df.groupby('Churn')['MonthlyCharges'].mean()
        ax1.bar(['Stayed', 'Churned'], churn_contract.values,
                color=['#2ecc71', '#e74c3c'], edgecolor='white')
        ax1.set_ylabel("Avg Monthly Charges ($)")
        ax1.set_title("Avg Monthly Charges by Churn Status")
        st.pyplot(fig1)
        plt.close()

    with col_b:
        st.subheader("Tenure distribution")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        df[df['Churn']==0]['tenure'].hist(
            ax=ax2, bins=30, alpha=0.6, color='#2ecc71', label='Stayed')
        df[df['Churn']==1]['tenure'].hist(
            ax=ax2, bins=30, alpha=0.6, color='#e74c3c', label='Churned')
        ax2.set_xlabel("Tenure (months)")
        ax2.set_ylabel("Count")
        ax2.legend()
        ax2.set_title("Tenure Distribution by Churn Status")
        st.pyplot(fig2)
        plt.close()

    st.markdown("---")

    st.subheader("Top churn drivers")
    feature_names = df.drop(columns=['Churn']).columns
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False).head(10)

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=importance_df, x='Importance', y='Feature',
                palette='Reds_r', ax=ax3)
    ax3.set_title("Top 10 Churn Drivers — Random Forest")
    st.pyplot(fig3)
    plt.close()

elif page == "Customer Segments":

    st.title("Customer Segments")
    st.markdown("Explore churn rates across different customer groups.")
    st.markdown("---")

    segment = st.selectbox(
        "Choose a segment to explore",
        ["Contract type", "Internet service",
         "Payment method", "Senior citizen", "Total services"]
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    if segment == "Contract type":
        data = df.groupby('Contract_Two year')['Churn'].mean() * 100
        labels = ['Month-to-month / One year', 'Two year']
        ax.bar(labels, data.values, color=['#e74c3c', '#2ecc71'], edgecolor='white')
        ax.set_title("Churn Rate: Two-year vs Other Contracts")

    elif segment == "Internet service":
        data = df.groupby('InternetService_Fiber optic')['Churn'].mean() * 100
        labels = ['DSL / No internet', 'Fiber optic']
        ax.bar(labels, data.values, color=['#2ecc71', '#e74c3c'], edgecolor='white')
        ax.set_title("Churn Rate by Internet Service Type")

    elif segment == "Payment method":
        data = df.groupby('PaymentMethod_Electronic check')['Churn'].mean() * 100
        labels = ['Other methods', 'Electronic check']
        ax.bar(labels, data.values, color=['#2ecc71', '#e74c3c'], edgecolor='white')
        ax.set_title("Churn Rate: Electronic Check vs Other Payment Methods")

    elif segment == "Senior citizen":
        data = df.groupby('SeniorCitizen')['Churn'].mean() * 100
        labels = ['Non-senior', 'Senior']
        ax.bar(labels, data.values, color=['#2ecc71', '#e74c3c'], edgecolor='white')
        ax.set_title("Churn Rate by Senior Citizen Status")

    elif segment == "Total services":
        data = df.groupby('total_services')['Churn'].mean() * 100
        ax.bar(data.index, data.values, color='#e74c3c', edgecolor='white', alpha=0.8)
        ax.set_xlabel("Number of Services")
        ax.set_title("Churn Rate by Number of Services Subscribed")

    ax.set_ylabel("Churn Rate (%)")
    ax.set_ylim(0, 80)
    for i, v in enumerate(data.values):
        ax.text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')
    st.pyplot(fig)
    plt.close()

    st.markdown("---")
    st.subheader("Raw numbers")
    st.dataframe(
        df.groupby('Churn').agg(
            Customers=('Churn', 'count'),
            Avg_Monthly=('MonthlyCharges', 'mean'),
            Avg_Tenure=('tenure', 'mean'),
            Avg_Services=('total_services', 'mean')
        ).round(2).rename(index={0: 'Stayed', 1: 'Churned'})
    )

elif page == "Churn Predictor":

    st.title("Live Churn Predictor")
    st.markdown("Enter a customer's details to predict their churn probability.")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        tenure = st.slider("Tenure (months)", 0, 72, 12)
        monthly_charges = st.slider("Monthly charges ($)", 18, 120, 65)
        total_charges = monthly_charges * tenure

    with col2:
        senior = st.selectbox("Senior citizen", ["No", "Yes"])
        partner = st.selectbox("Has partner", ["No", "Yes"])
        dependents = st.selectbox("Has dependents", ["No", "Yes"])

    with col3:
        contract_2yr = st.selectbox("Contract type",
                                     ["Month-to-month / One year", "Two year"])
        internet = st.selectbox("Internet service",
                                 ["DSL / None", "Fiber optic"])
        num_services = st.slider("Number of add-on services", 0, 6, 2)

    input_dict = {col: 0 for col in df.drop(columns=['Churn']).columns}

    input_dict['tenure'] = tenure
    input_dict['MonthlyCharges'] = monthly_charges
    input_dict['TotalCharges'] = total_charges
    input_dict['SeniorCitizen'] = 1 if senior == "Yes" else 0
    input_dict['Partner'] = 1 if partner == "Yes" else 0
    input_dict['Dependents'] = 1 if dependents == "Yes" else 0
    input_dict['total_services'] = num_services
    input_dict['charges_per_tenure'] = monthly_charges / (tenure + 1)
    input_dict['high_spender'] = 1 if monthly_charges > 64 else 0
    input_dict['Contract_Two year'] = 1 if contract_2yr == "Two year" else 0
    input_dict['InternetService_Fiber optic'] = 1 if internet == "Fiber optic" else 0

    input_df = pd.DataFrame([input_dict])

    st.markdown("---")

    if st.button("Predict churn risk", type="primary"):
        prob = model.predict_proba(input_df)[0][1]
        prediction = "High risk" if prob > 0.5 else "Low risk"
        color = "🔴" if prob > 0.5 else "🟢"

        st.markdown(f"### {color} {prediction}")
        st.metric("Churn probability", f"{prob*100:.1f}%")

        fig, ax = plt.subplots(figsize=(8, 1.5))
        ax.barh(['Risk'], [prob], color='#e74c3c', height=0.4)
        ax.barh(['Risk'], [1 - prob], left=[prob],
                color='#2ecc71', height=0.4)
        ax.set_xlim(0, 1)
        ax.axvline(0.5, color='gray', linestyle='--', linewidth=1)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'])
        ax.set_title("Churn probability")
        st.pyplot(fig)
        plt.close()

        if prob > 0.5:
            st.warning(
                "**Retention recommendation:** This customer is at high risk. "
                "Consider offering a contract upgrade incentive or a loyalty discount "
                "within the next 30 days."
            )
        else:
            st.success(
                "**Low risk customer.** Standard engagement is sufficient. "
                "Monitor at next quarterly review."
            )