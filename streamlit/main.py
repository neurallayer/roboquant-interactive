import streamlit as st
from streamlit.web.bootstrap import run
import roboquant as rq
import pandas as pd


st.title(f"roboquant version {rq.__version__}")

st.markdown("## Feed Configuration")
start_date = st.date_input("Start Date", value="2010-01-01")
symbols_str = st.text_input("Symbols", value="TSLA, IBM, AAPL, MSFT, JPM, GOOGL")
symbols = [s.strip().upper() for s in symbols_str.split(",")]

if st.button("Load Data", type="primary"):
    st.session_state.clear()
    st.session_state.feed = rq.feeds.YahooFeed(*symbols, start_date=start_date)

if feed := st.session_state.get("feed"):
    assert isinstance(feed, rq.feeds.YahooFeed)
    st.markdown("## Price Viewer")
    assets = {asset.symbol: asset for asset in feed.assets()}
    symbol = st.selectbox("Symbol", options=assets.keys())
    asset = assets[symbol]

    x, y = feed.get_prices(asset)
    st.line_chart({"time": x, "price": y}, x="time", y="price")

    st.markdown("## Back Test Config")
    strategies = { f"EMA-{x}-{y}" : (x, y) for (x, y) in [(3,5), (7,15), (12, 25), (25, 50)]}
    strategy_name = st.selectbox("Strategy", options=strategies.keys())
    strategy_params = strategies[strategy_name]

    if st.button("Run Back Test", type="primary"):
        strategy = rq.strategies.EMACrossover(*strategy_params)
        journal = rq.journals.MetricsJournal.pnl()
        account = rq.run(feed, strategy, journal=journal)
        st.session_state.account = account
        st.session_state.journal = journal

    if account := st.session_state.get("account"):
        assert isinstance(account, rq.Account)
        st.markdown("## Account")
        st.write(account)
        st.markdown("## Open Orders")
        df = pd.DataFrame(account.get_order_list())
        st.write(df)
        st.markdown("## Open Positions")
        df = pd.DataFrame(account.get_position_list())
        st.write(df)

    if journal := st.session_state.get("journal"):
        assert isinstance(journal, rq.journals.MetricsJournal)
        st.markdown("## Metrics")
        metric_name = st.selectbox("Metric", options=journal.get_metric_names())
        x, y = journal.get_metric(metric_name)
        st.line_chart({"time": x, "values": y}, x="time", y="values")

if __name__ == "__main__":

    # this file will run itself, but the second time this check is False 
    # to stop the startup of a second instance
    if '__streamlitmagic__' not in locals():
        run(__file__, False, [], {})