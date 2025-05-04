import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide")
#CSS styles
st.markdown("""
<style>
    .header-title {
    background: linear-gradient(to right, #81c784, #66bb6a);
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    }
    .header-title h1 {
        color: white;
        margin: 0;
        font-size: 36px;
        font-family: 'Segoe UI', sans-serif;
    }
    .insight-card {
        padding: 20px;
        border-radius: 20px;
        color: white;  
        font-family: 'Arial', sans-serif;
        font-size: 1.2em;
        text-align: center;
        height: 170px;
        display: flex;
        flex-direction: column;
        justify-content: center;   
    }
    .card-blue { background-color: #1f77b4; }
    .card-green {
        background-color: #2ca02c;
        font-size: 0.8em;
    }
    .card-red { background-color: #d62728; }
    .card-purple { background-color: #9467bd; }
    .card h4 {
        margin-bottom: 10px;
        font-weight: normal;
    }
    .card h2 {
        margin: 0;
        font-size: 2em;
    }
</style>
""", unsafe_allow_html=True)


# Set title
st.markdown("""
<div class="header-title">
    <h1>🚲 Bike Networks Data Visualization</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>",unsafe_allow_html=True)


# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("final_bike_networks.csv",header=0)
    df = df.sort_values('Station Count', ascending=False).reset_index(drop=True)  #sort by station count
    return df

df = load_data()

# Calculate key metrics
total_networks = len(df)

country_station_totals = df.groupby("Country Name", as_index=False)["Station Count"].sum()
top_country = country_station_totals.sort_values("Station Count", ascending=False).iloc[0]

top_network = df.loc[df["Station Count"].idxmax()]

total_stations = df["Station Count"].sum()

# Display key metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="insight-card card-blue card">
        <h4>Total Networks</h4>
        <h2>{total_networks:,}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="insight-card card-green card">
        <h4>Top Country (Total Stations)</h4>
        <h2>{top_country['Country Name']} ({int(top_country['Station Count']):,})</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="insight-card card-red card">
        <h4>Top Network</h4>
        <h2>{top_network['Network Name']}</h2>
        <p style="font-size:16px;">{top_network['Station Count']:,} stations</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="insight-card card-purple card">
        <h4>Total Stations</h4>
        <h2>{total_stations:,}</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>",unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1])  
# left section for bar chart and pie chart (top 5 networks)
with left_col:

    st.markdown("### 📊 Number of Stations for each Bike Network")
    page_size = 10
    total_pages = (len(df) - 1) // page_size

    # Keep track of page in session state
    if "page" not in st.session_state:
        st.session_state.page = 0

    # Create navigation buttons
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("⬅️ Previous") and st.session_state.page > 0:
            st.session_state.page -= 1
    with col3:
        if st.button("Next ➡️") and st.session_state.page < total_pages:
            st.session_state.page += 1

    # Slice current visible data
    start = st.session_state.page * page_size
    end = start + page_size
    visible_df = df.iloc[start:end].copy()

    # Dynamic local max for rescaling bars
    local_max = visible_df["Station Count"].max()

    # Create bar chart
    fig = px.bar(
        visible_df.sort_values("Station Count"),
        x="Station Count",
        y="Network_id",
        orientation="h",
        labels={"Station Count": "Station Count", "Network_id": "Name of Network"},
        title=f"Bike Networks {start + 1} to {min(end, len(df))}",
        template="seaborn",
        text="Station Count",
    )
    # styling the bar chart
    fig.update_layout(
        xaxis=dict(range=[0, local_max * 1.1],showticklabels=False),
        yaxis=dict(title=''),
        height=380,
        plot_bgcolor='#d6eaf8',
        paper_bgcolor='#d6eaf8',
        font=dict(color='black',family='Arial')
    )
    
    st.plotly_chart(fig, use_container_width=True)  # Display the bar chart

    st.markdown("### Top 5 Networks by Number of Stations")
    top_5_networks = df.sort_values("Station Count", ascending=False).head(5)

    # create pie chart
    fig_pie_top5 = px.pie(
        top_5_networks,
        names="Network Name",
        values="Station Count",
        hole=0.4 
    )

    fig_pie_top5.update_traces(
        textinfo='value+label',
        pull=[0.05]*5  # adds slight separation between slices
    )

    fig_pie_top5.update_layout(
        height=450,
        plot_bgcolor="#ebdef0",    
        paper_bgcolor="#ebdef0",
    )

    st.plotly_chart(fig_pie_top5, use_container_width=True)

# right section for average number of stations per country and pie chart (top 5 countries)
with right_col:
    st.markdown("### 🌍 Avg Number of Stations per Country")
    
    avg_per_country = df.groupby("Country Name", as_index=False)["Station Count"].mean()
    avg_per_country = avg_per_country.sort_values("Station Count", ascending=False)
    avg_per_country["Station Count"] = avg_per_country["Station Count"].round(0).astype(int)
    avg_per_country = avg_per_country.rename(columns={"Station Count": "Number of Stations"})

    st.dataframe(avg_per_country, use_container_width=True, hide_index=True)

    st.markdown("<br>",unsafe_allow_html=True)

    st.markdown("### Top 5 Countries by Number of Stations")
    top_5_countries = (
    df.groupby("Country Name", as_index=False)["Station Count"]
    .sum()
    .sort_values("Station Count", ascending=False)
    .head(5)   
    )

    # pie chart
    fig_pie = px.pie(
        top_5_countries,
        values="Station Count",
        names="Country Name",
        hole=0.4 
    )

    # Update style
    fig_pie.update_traces(textinfo='percent+label', pull=[0.05]*5)
    fig_pie.update_layout(
        height=450, 
        plot_bgcolor="#fdf2e9",  
        paper_bgcolor="#fdf2e9", 
    )

    # Display chart
    st.plotly_chart(fig_pie, use_container_width=True)

    




