import streamlit as st
import json
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Smart Meter Dashboard", layout="wide")

# Load YOUR data
@st.cache_data
def load_data():
    with open('dashboard_data.json', 'r') as f:
        return json.load(f)

data = load_data()

# Header
st.title("🏠 Smart Meter Analysis Dashboard")
st.markdown("**Electricity consumption patterns & appliance insights**")

# KPIs 
col1, col2, col3, col4 = st.columns(4)
col1.metric("Houses", data['houses'])
col2.metric("Peak Hour", f"{data['peak_hour']}:00")
col3.metric("Peak Demand", f"{data['peak_demand']:.1f} kWh")
col4.metric("Records", f"{data['total_records']:,}")

# Charts Row 1
col1, col2 = st.columns(2)
with col1:
    st.subheader("⏰ Hourly Pattern")
    hours = list(data['hourly_avg'].keys())
    demand = list(data['hourly_avg'].values())
    fig1 = px.line(x=hours, y=demand, title="Avg Demand by Hour", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📅 Monthly Usage")
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    monthly = [data['monthly_avg'].get(i+1, 0) for i in range(12)]
    fig2 = px.bar(x=months, y=monthly, title="Avg Demand by Month")
    st.plotly_chart(fig2, use_container_width=True)

# Charts Row 2
col1, col2 = st.columns(2)
with col1:
    st.subheader("🌤️ Weather Impact")
    weather = list(data['weather_avg'].keys())
    wdemand = list(data['weather_avg'].values())
    fig3 = px.bar(x=weather, y=wdemand, title="Demand by Weather")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("🏖️ Seasonal")
    fig4 = px.bar(x=list(data['season_avg'].keys()), y=list(data['season_avg'].values()), title="Demand by Season")
    st.plotly_chart(fig4, use_container_width=True)

# Appliances
st.subheader("🔌 Appliance Usage")
col1, col2 = st.columns(2)
means = data['appliance_means']
appliances = ['Washing_Mach','Microwave','TV','Dishwasher','sum_appliances','unallocated']
values = [means[a] for a in appliances]

with col1:
    fig5 = px.pie(values=values, names=appliances, title="Appliance Share")
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.markdown("**Insights:**")
    top_app = max(appliances, key=lambda x: means[x])
    st.success(f"🚀 Top: **{top_app}** ({means[top_app]:.1f} kWh)")
    st.info(f"⚠️ Unallocated: **{means['unallocated']/means['demand']*100:.1f}%**")

# Recommendations
st.subheader("💡 Tariff Recommendations")
st.markdown("""
- **Peak {data['peak_hour']}** → **Time-of-Use tariff** (night cheaper)
- **High washing machine** → Schedule **off-peak**
- **Weather sensitive** → Consider **fixed rate**
""")

# 🔥 ADD THIS NEW SECTION (after your existing charts)
st.markdown("---")
st.subheader("🚀 Business Insights")

col1, col2, col3 = st.columns(3)
col1.metric("Base Load Waste", f"€{(data['base_load']*24*365*0.30):.0f}/yr")
col2.metric("Washing Machine", f"€{data['washing_annual_cost']:.0f}/yr") 
col3.metric("Total Savings", f"€{data['total_savings_potential']:.0f}/yr")

st.success(f"""
**Key Recommendations:**
• Peak {data['peak_hour']}:00 → **Time-of-Use tariff** 
• Base load {data['base_load']:.1f}kWh → **€{int(data['base_load']*24*365*0.30)} standby waste**
• Cold +{data['cold_weather_pct']:.0f}% demand → **Fixed rate hedge**
**Scale to 1000 houses = €{int(data['total_savings_potential']*1000):,} opportunity**
""")
