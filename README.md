
# ![roboquant logo](https://github.com/neurallayer/roboquant.py/raw/main/docs/roboquant_header.png)

![PyPI - Version](https://img.shields.io/pypi/v/roboquant?label=roboquant)
![PyPI - License](https://img.shields.io/pypi/l/roboquant)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/roboquant)
![PyPI - Status](https://img.shields.io/pypi/status/roboquant)
[![discord](https://img.shields.io/discord/954650958300856340?label=discord)](https://discord.com/channels/954650958300856340/954650958300856343)

Roboquant is an open-source algorithmic trading platform. It is flexible, user-friendly and completely free to use. It is designed for anyone serious about algo-trading. 

So whether you are a beginning retail trader or an established trading firm, roboquant can help you to develop robust and fully automated trading strategies. You can find out more at [roboquant.org](https://roboquant.org).


# Usage
This repo contains a number of Python Jupyter Notebooks that demonstrate hwo to use roboquant. 

If you don't want to install anything local, you can try roboquant in an online Jupyter environment [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/neurallayer/roboquant-notebooks/HEAD?labpath=%2Fintro_roboquant.ipynb)

 
Otherwise, you can install roboquant including one or more of the optional dependencies if you require certain functionality:

```shell
# market data from Yahoo Finance using the YahooFeed
python3 -m pip install --upgrade "roboquant[yahoo]"

# PyTorch based strategies using RNNStrategy
python3 -m pip install --upgrade "roboquant[torch]"

# Integration with Interactive Brokers using IBKRBroker
python3 -m pip install --upgrade "roboquant[ibkr]"

# Install all dependencies
python3 -m pip install --upgrade "roboquant[all]"
```


## License
These notebooks are made available under the Apache 2.0 license. You can read more about the Apache 2.0 license on this page: https://www.apache.org/licenses/LICENSE-2.0.html

## Disclaimer
Absolutely no warranty is implied with this product. Use at your own risk. I provide no guarantee that it will be profitable, or that it won't lose all your money very quickly or doesn't contain bugs. All financial trading offers the possibility of loss. Leveraged trading, may result in you losing all your money, and still owing more. Backtested results are no guarantee of future performance. I can take no responsibility for any losses caused by live trading using roboquant. Use at your own risk. I am not registered or authorised by any financial regulator.

