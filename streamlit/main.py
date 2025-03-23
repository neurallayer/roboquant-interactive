import streamlit as st
import roboquant as rq
from matplotlib import pyplot as plt
import pandas as pd


st.title(f"roboquant version {rq.__version__}")

st.markdown("## Feed Configuration")
start_date = st.date_input("Start Date", value="2010-01-01")
symbols_str = st.text_input("Symbols", value="TSLA, IBM, AAPL, MSFT, JPM, GOOGL")

symbols = [s.strip() for s in symbols_str.split(",")]
feed = rq.feeds.YahooFeed(*symbols, start_date=str(start_date))

if st.button("Load Data", type="primary"):
    feed = rq.feeds.YahooFeed(*symbols, start_date=str(start_date))
    st.session_state.clear()
    st.session_state.feed = feed
    
if feed := st.session_state.get("feed"):
    st.markdown("## Price Viewer")
    assets = {asset.symbol:asset for asset in feed.assets()}
    symbol = st.selectbox("Symbol", options=assets.keys())
    fig, ax = plt.subplots()
    feed.plot(assets[symbol], ax=ax)
    st.pyplot(fig)

    if st.button("Run Back Test", type="primary"):
        strategy = rq.strategies.EMACrossover()
        journal = rq.journals.MetricsJournal.pnl()
        account = rq.run(feed, strategy, journal=journal)
        st.session_state.account = account
        st.session_state.journal = journal

    if  account := st.session_state.get("account"):
        st.markdown("## Account")
        st.write(account)
        df = pd.DataFrame(account.get_positions_list())
        st.markdown("## Open Positions")
        st.write(df)

    if journal := st.session_state.get("journal"):
        st.markdown("## Metrics")
        metric_name = st.selectbox("Metric", options=journal.get_metric_names())
        fig, ax = plt.subplots()
        journal.plot(metric_name, ax=ax)
        st.pyplot(fig)