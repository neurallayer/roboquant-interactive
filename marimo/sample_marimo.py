import marimo

__generated_with = "0.11.26"
app = marimo.App(width="medium", app_title="roboquant demo")


@app.cell
async def _():
    import marimo as mo
    import micropip # type: ignore
    await micropip.install("roboquant==1.6.0")
    import roboquant as rq
    import pandas as pd
    from matplotlib import pyplot as plt
    plt.rcParams["figure.figsize"] = (10,6)
    mo.md(f"# roboquant version {rq.__version__}")
    return micropip, mo, pd, plt, rq


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
    return asset_options, asset_selector


@app.cell
def _(asset_selector, feed, mo, plt):
    feed.plot(asset_selector.value)

    mo.vstack([
        mo.md("## Stock Price Viewer"), 
        asset_selector,
        mo.mpl.interactive(plt.gca())
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
    return account, journal, strat


@app.cell
def _(account, mo):
    mo.md(f"## Account \n<pre>{account}</pre>")
    return


@app.cell
def _(account, mo, pd):
    df_orders = pd.DataFrame(account.get_order_list())
    mo.md(f"## Open Orders {mo.as_html(df_orders)}")
    return (df_orders,)


@app.cell
def _(account, mo, pd):
    df_positions = pd.DataFrame(account.get_position_list())
    mo.md(f"## Open Positions {mo.as_html(df_positions)}")
    return (df_positions,)


@app.cell
def _(journal, mo):
    options = list(journal.get_metric_names())
    radio = mo.ui.radio(options=options, value = "pnl/equity", label="Select a metric")
    mo.md(f"## Metrics")
    return options, radio


@app.cell
def _(journal, mo, plt, radio):
    journal.plot(radio.value)

    mo.hstack(
        [
            radio, 
            mo.mpl.interactive(plt.gca())
        ], widths=[1, 4])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
