import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Tarun.Streamlit')

df = pd.read_csv('startup_cleaned (1).csv')

st.sidebar.title("Startup Funding Analysis")
st.title('Indian StartUps Funding Analysis(2015-2020)')

def load_investor_details(investor):
    st.title(investor)
    #investments of investor
    data_df = df[df["Investors"].str.contains(investor)][['Date', 'Startup', 'Vertical', 'City', 'Investors', 'Investment Type', 'Amount in CR']]
    st.dataframe(data_df)

    #sectors invested in
    st.title("Sectors Invested in")
    pie_series = df[df['Investors'].str.contains(investor)].groupby('Vertical')['Amount in CR'].sum()

    fig, ax = plt.subplots()
    ax.pie(pie_series, labels=pie_series.index, rotatelabels=True, labeldistance=1.5)

    st.pyplot(fig)


    col1 = st.columns()
    with col1:
        st.title("Biggest 5 Investment")
        # biggest investment
        big_series = df[df["Investors"].str.contains(investor)].groupby('Startup')['Amount in CR'].sum().sort_values(ascending=False).head(5)

        fig1, ax1 = plt.subplots()
        ax1.bar(big_series.index, big_series.values)
        ax1.set_title('Top 5 Investments of investor')
        ax1.set_xlabel('StartUps')
        ax1.set_ylabel('Amount(CR)')
        st.pyplot(fig1)
    col1 = st.columns(1)
    with col1:
        st.title("Investment Type")
        stage_series = df[df['Investors'].str.contains(investor)].groupby('Investment Type')['Amount in CR'].sum()

        fig1, ax1 = plt.subplots()
        ax1.pie(stage_series, labels=stage_series.index, autopct='%0.01f%%',rotatelabels=True,labeldistance=1.5)

        st.pyplot(fig1)

    col1 = st.columns(1)
    with col1:
        st.title("Invested Cities")
        city_series = df[df['Investors'].str.contains(investor)].groupby('City')['Amount in CR'].sum()

        fig1, ax1 = plt.subplots()
        ax1.pie(city_series, labels=city_series.index, autopct='%0.01f%%',rotatelabels=True,labeldistance=1.5)

        st.pyplot(fig1)
    col1 = st.columns(1)
    with col1:
        st.title('YOY Investment Analysis')
        df['Year'] = pd.to_datetime(df['Date'], dayfirst=True).dt.year
        year_series = df[df['Investors'].str.contains(investor)].groupby('Year')['Amount in CR'].sum()

        fig1, ax1 = plt.subplots()
        ax1.plot(year_series.index,year_series.values)

        st.pyplot(fig2)

def load_overall_analysis():
    st.title('Overall Analysis')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        #total amount invested
        total = round(df['Amount in CR'].sum())
        st.metric('Total',str(total) + ' Cr')

    with col2:
        #max funding raised startup
        max_funding = df.groupby('Startup')['Amount in CR'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Max',str(max_funding) + ' Cr')

    with col3:
        #avg funding
        avg_fund = round(df.groupby('Startup')['Amount in CR'].sum().mean())
        st.metric('Avg Funding in India',str(avg_fund) + ' Cr')

    with col4:
        #total funded startups
        total_funded = df['Startup'].nunique()
        st.metric('Total Funded Startups', total_funded)

    #--
    st.title('Month-on-Month Graph')

    select_input = st.selectbox('Select Type',['StartUps per Month','Amount Funded per Month'])
    if select_input == 'StartUps per Month':

        df['Year'] = pd.to_datetime(df['Date'], dayfirst=True).dt.year
        df['month'] = pd.to_datetime(df['Date'], dayfirst=True).dt.month
        temp_df = df.groupby(['Year', 'month'])['Startup'].count().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['Year'].astype('str')

        fig5, ax5= plt.subplots(figsize=(7,3))
        ax5.bar(temp_df['x_axis'], temp_df['Startup'])
        ax5.set_title('Total Funded StartUps per Month')
        ax5.set_ylabel('No. of StartUps')
        ax5.set_xlabel('Month-Year')
        # ax5.set_ticks(rotation='vertical')
        # ax5.legend()

        st.pyplot(fig5)

    else:

        df['Year'] = pd.to_datetime(df['Date'], dayfirst=True).dt.year
        df['month'] = pd.to_datetime(df['Date'], dayfirst=True).dt.month
        temp_df1 = df.groupby(['Year', 'month'])['Amount in CR'].sum().reset_index()
        temp_df1['x_axis'] = temp_df1['month'].astype('str') + '-' + temp_df1['Year'].astype('str')

        fig5, ax5 = plt.subplots(figsize=(7, 3))
        ax5.plot(temp_df1['x_axis'], temp_df1['Amount in CR'])

        ax5.set_title('Total Amount Funded per Month')
        ax5.set_ylabel('Amount (in CR)')
        ax5.set_xlabel('Month-Year')
        # ax5.set_xticks(rotation='vertical')
        # ax5.legend()

        st.pyplot(fig5)


option = st.sidebar.selectbox("Select One", ["Overall Analysis", "StartUp", "Investor"])

if option == 'Overall Analysis':
    load_overall_analysis()



elif option == 'StartUp':
    st.sidebar.selectbox('Select StartUp', sorted(df['Startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp details')
    st.title("StartUp Analysis")

elif option == 'Investor':
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['Investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor details')
    if btn2:
        load_investor_details(selected_investor)


