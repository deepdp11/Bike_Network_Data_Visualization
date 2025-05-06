import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# CSS styles
st.markdown("""
<style>
    .header-title {    
        background-color: #3498db;
        padding: 1px;
        border-radius: 10px;
        text-align: center;
    }
    .header-title h1 {
        color: white;
        margin: 0;
        font-size: 36px;
        font-family: 'Arial', sans-serif;
    }
    .insight-card {
        padding: 20px;
        border-radius: 20px;
        color: white;  
        font-family: 'Arial', sans-serif;
        text-align: center;
        height: 170px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        overflow: hidden;
    }
    .card-blue { background-color: #1f77b4; }
    .card-green {
        background-color: #2ca02c;
        font-size: 0.8em;
    }
    .card-red { background-color: #e74c3c; }
    .card-purple { background-color: #9467bd; }
    .card h4 {
        margin-bottom: 10px;
        font-weight: normal;
        font-size: clamp(0.9rem, 1.5vw, 1.2rem);
        white-space: normal;
        word-wrap: break-word;
    }
    .card h2 {
        margin: 0;
        font-size: clamp(1.2rem, 2.5vw, 2rem); 
        white-space: normal;  
        word-wrap: break-word;
    }
    .section-title {
        font-size: 24px;
        font-weight: 600;
        color: black;
        background-color: #F4F9E7;
        padding: 12px 20px;
        border-radius: 8px;
        margin-top: 25px;
        font-family: 'Segoe UI', sans-serif;
        border-radius: 20px 20px 0px 0px;
    }
    .section-title-purple {
        font-size: 20px;
        font-weight: 600;
        background-color: #ebdef0;
        color: #4a235a;
        padding: 10px 16px;
        font-family: 'Segoe UI', sans-serif;
        border-radius: 20px 20px 0px 0px;
    }

    .section-title-orange {
        font-size: 20px;
        font-weight: 600;
        background-color: #fdf2e9;
        color: #784212;
        padding: 10px 16px;
        font-family: 'Segoe UI', sans-serif;
        border-radius: 20px 20px 0px 0px;
    }
    .footer {
        margin-top: 40px;
        padding-top: 10px;
        border-top: 1px solid #ccc;
        text-align: center;
        color: #555;
        font-size: 14px;
        font-family: 'Segoe UI', sans-serif;
    }

    .footer a {
        color: #2e86c1;
        text-decoration: none;
    }

    .footer a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<div class="header-title">
    <h1>🚲 City Bike Dashboard</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("final_bike_networks.csv", header=0)
    df = df.sort_values('Station Count', ascending=False).reset_index(drop=True)
    df["Country Name"] = df["Country Name"].astype(str).str.strip()
    return df

df = load_data()
table_df = df.copy()

# country filter
country_list = sorted(df["Country Name"].dropna().unique())
selected_country = st.selectbox("Select Country", options=["All"] + country_list)

if selected_country != "All":
    df = df[df["Country Name"] == selected_country]

# Calculate metrics
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

st.markdown("<br>", unsafe_allow_html=True)


# Top 5 Cities Pie Chart
top_5_cities = (
    df.groupby("City", as_index=False)["Station Count"]
    .sum()
    .sort_values("Station Count", ascending=False)
    .head(5)
)
fig_city_pie = px.pie(
    top_5_cities,
    values="Station Count",
    names="City",
    hole=0.4,
)
fig_city_pie.update_traces(textinfo='value', pull=[0.05]*5)
fig_city_pie.update_layout(height=400, plot_bgcolor="#ebdef0", paper_bgcolor="#ebdef0")

# Top 5 Networks Pie Chart

top_5_networks = df.sort_values("Station Count", ascending=False).head(5)
fig_network_pie = px.pie(
    top_5_networks,
    names="Network_id",
    values="Station Count",
    hole=0.4,
)
fig_network_pie.update_traces(textinfo='value', pull=[0.05]*5)
fig_network_pie.update_layout(height=400, plot_bgcolor="#fdf2e9", paper_bgcolor="#fdf2e9")

# Display pie charts side-by-side
col1, col2 = st.columns(2)
with col1:
    city_pie_title = (f"🏙️ Top Cities by Number of Stations in {selected_country}" if selected_country != "All" else "🏙️ Top Cities by Number of Stations")
    st.markdown(f"<div class='section-title-purple'>{city_pie_title}</div>", unsafe_allow_html=True)
    st.plotly_chart(fig_city_pie, use_container_width=True)

with col2:
    network_pie_title = (f"🥇 Top Networks by Number of Stations in {selected_country}" if selected_country != "All" else "🥇 Top Networks by Number of Stations")
    st.markdown(f"<div class='section-title-orange'>{network_pie_title}</div>", unsafe_allow_html=True)
    st.plotly_chart(fig_network_pie, use_container_width=True)

# Display bar chart of stations per network and average stations per country side-by-side
left_col, right_col = st.columns(2)
with left_col:
    # Bar chart of stations per network
    page_size = 10
    total_pages = (len(df) - 1) // page_size + 1

    if "page" not in st.session_state:
        st.session_state.page = 0

    # Navigation buttons for bar chart
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("⬅️ Previous") and st.session_state.page > 0:
            st.session_state.page -= 1
    with col3:
        if st.button("Next ➡️") and st.session_state.page < total_pages - 1:
            st.session_state.page += 1

    # Slice data for current page
    start = st.session_state.page * page_size
    end = start + page_size
    paged_df = df.iloc[start:end].copy()

    # Bar Chart title
    title_text = f"📊 Number of Stations for Each Bike Network in {selected_country}" if selected_country != "All" else "📊 Number of Stations for Each Bike Network"
    st.markdown(f"<div class='section-title'>{title_text}</div>", unsafe_allow_html=True)

    # Create bar chart
    fig = px.bar(
        paged_df.sort_values("Station Count", ascending=False),
        x="Station Count",
        y="Network_id",
        orientation="h",
        color="Network_id",  
        color_discrete_sequence=px.colors.sequential.Tealgrn,
        labels={"Station Count": "Station Count", "Network_id": "Name of Network"},
        title=f"Bike Networks {start + 1} to {min(end, len(df))} in {selected_country}" if selected_country != "All" else f"Bike Networks {start + 1} to {min(end, len(df))} (All Countries)",
        template="seaborn",
        text="Station Count",
    )
    #hide legend
    fig.for_each_trace(lambda t: t.update(showlegend=False))

    # Update layout
    local_max = paged_df["Station Count"].max()
    fig.update_layout(
        xaxis=dict(range=[0, local_max * 1.1], showticklabels=False),
        yaxis=dict(title='', tickfont=dict(color='black', family='Arial', size=13)),
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='#F4F9E7',
        font=dict(color='black', family='Arial'),
    )

    # Show chart
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    # Average stations per country
    st.markdown("### 🌍 Avg Number of Stations per Country")
    # calculate average stations per country    
    avg_per_country = table_df.groupby("Country Name", as_index=False)["Station Count"].mean()
    avg_per_country = avg_per_country.sort_values("Station Count", ascending=False)
    avg_per_country["Station Count"] = avg_per_country["Station Count"].round(0).astype(int)
    avg_per_country = avg_per_country.rename(columns={"Station Count": "Number of Stations"})
    # display average stations per country
    st.dataframe(avg_per_country, use_container_width=True, hide_index=True)

    st.markdown("<br>",unsafe_allow_html=True)


# Display data table
st.markdown(f"### 📊 Data of Bike Networks in {selected_country}" if selected_country != "All" else "### 📊 Data of Bike Networks")
st.dataframe(df, use_container_width=True, hide_index=True)

st.download_button(
    label="📥 Download Data as CSV",
    data=df.to_csv(index=False),
    file_name=f"bike_network_data_{selected_country}.csv",
    mime="text/csv"
)

# Footer
st.markdown("""
<div class="footer">
    Developed by Deep Patel, Data sourced from 
    <a href="http://api.citybik.es/v2/networks" target="_blank">CityBikes API</a>
</div>
""", unsafe_allow_html=True)
