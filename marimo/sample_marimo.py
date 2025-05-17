import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium", app_title="roboquant demo")


@app.cell
def _():
    import marimo as mo
    import altair as alt
    import roboquant as rq
    import pandas as pd
    from matplotlib import pyplot as plt
    plt.rcParams["figure.figsize"] = (10,6)
    mo.md(f"# roboquant version {rq.__version__}")
    return alt, mo, pd, rq


@app.cell
def _(mo):
    symbols_input = mo.ui.slider(start=1, stop=100, value=10, label="Number of stocks")
    start_date = mo.ui.date(start="2020-01-01", label="start date")
    mo.md(f"##Feed Configuration \n{symbols_input} {start_date}")
    return start_date, symbols_input


@app.cell
def _(rq, start_date, symbols_input):
    feed = rq.feeds.RandomWalk(n_symbols = symbols_input.value, start_date=start_date.value)
    assets = feed.assets()
    return assets, feed


@app.cell
def _(assets, mo):
    asset_options = { asset.symbol:asset for asset in assets}
    asset_selector = mo.ui.dropdown(asset_options, value = assets[0].symbol, label = "Select a symbol")
    return (asset_selector,)


@app.cell
def _(alt, asset_selector, feed, mo):
    data = feed.to_dataframe(asset_selector.value).reset_index(names="time")
    chart = alt.Chart(data).mark_line().encode(
        x='time',
        y='Close'
    )
    chart = mo.ui.altair_chart(chart, chart_selection="interval")

    return (chart,)


@app.cell
def _(asset_selector, chart, mo):
    mo.vstack([
        mo.md("## Stock Price Viewer"), 
        asset_selector,
        chart,
        chart.value
    ])
    return


@app.cell
def _(mo):
    run_button = mo.ui.run_button(kind="success", label="Run Back Test")
    run_button
    return (run_button,)


@app.cell
def _(feed, mo, rq, run_button):
    mo.stop(not run_button.value)

    strat = rq.strategies.EMACrossover()
    journal = rq.journals.MetricsJournal.pnl()
    account = rq.run(feed, strat, journal=journal)
    return account, journal


@app.cell
def _(account, mo):
    mo.md(f"""## Account \n<pre>{account}</pre>""")
    return


@app.cell
def _(account, mo, pd):
    df_orders = pd.DataFrame(account.get_order_list())
    mo.md(f"## Open Orders {mo.as_html(df_orders)}")
    return


@app.cell
def _(account, mo, pd):
    df_positions = pd.DataFrame(account.get_position_list())
    mo.md(f"## Open Positions {mo.as_html(df_positions)}")
    return


@app.cell
def _(journal, mo):
    options = list(journal.get_metric_names())
    radio = mo.ui.radio(options=options, value = "pnl/equity", label="Select a metric")
    mo.md("## Metrics")
    return (radio,)


@app.cell
def _(alt, journal, mo, radio):
    df = journal.to_dataframe(radio.value)
    metric_chart = alt.Chart(df).mark_line().encode(
        x="time",
        y="value"
    )

    metric_chart = mo.ui.altair_chart(metric_chart, chart_selection="interval")
    return (metric_chart,)


@app.cell
def _(metric_chart, mo, radio):
    mo.hstack([
        radio, 
        mo.vstack([
            metric_chart,
            metric_chart.value
        ])    
    ], widths=[1, 4])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
