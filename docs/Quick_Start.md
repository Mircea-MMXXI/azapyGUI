# Quick Start #
## Installation ##

Package installation: *pip install azapyGUI*

## Start ##

To start the application you need to write the following 2-line python script. 
For the purpose of this example, let's call it `my_azapy.py`.

```python
import azapyGUI
azapyGUI.start()
```
Then run the script in a powershell as 
```
python my_azapy.py
```
This will bring up the main application panel.

![alt text](panels/Main_panel.png)

There are no active projects nor active market data for now. We will come back to these in a minute. 
For now, first thinks first. 

## Basic Setups ##

On the menu, click on `Settings` and then on `Application Settings`. 
The `User Default Settings` window will popup.

![alt text](panels/Settings_panel.png)

In the first tab, called `Directories`, you must make three choices.
1. `Portfolio Directory` - this is the default user directory where you can save/load portfolio/project files. 
When saving/loading a project, you will be prompt to this 
directory (you can always change it). 
2. `Market Data Directory` - local (buffer) market data directory. Once the historical data is retrieved form 
the provider, a copy is stored in this directory. Successive calls for the same market data will try first to access data from
this directory and then, and only if there is a need to update the data, from the provider. This will speed up considerable 
the computations (in general accessing repeatedly the same provider data over the internet may add up to a 
considerable amount of time). The market data stored in this directory is not intended to be consumed by other 
applications nor as a permanent storage. There are other mechanisms provided by `azapyGUI` for visualizing and 
analyzing the market data as well as for saving it in a variety of file formats. 
3. `Data Output Directory` - this is the default user directory where graphical and analytical reports can be 
saved for further inspection. 

Then press `Save` and close the window. 

These are persistent setups, preserved between `azapyGUI` sessions.


We will come back later to the topic of user settings with more details about the available options. 
For now this is all what we need to start the very first `azapyGUI` session.

## Build First Portfolio ##

Now we are back at the main panel and we will start to build the first portfolio project. 
On the menu click of the tab `Portfolio` and then click on item `New`. 

A `Portfolio Edit` window will popup.

![alt text](panels/PortfolioEdit_panel.png)

Here we will enter the portfolio information: name, components, and optimization model.
1. Name - on the entry space, right of label `Edit Portfolio`, replace the suggestion `MyPort` with 
    the name you want for this portfolio (try to chose something short and meaningful for you). For
    our example let us type `Port-MAD`. I know, it is not very inspiring or meaningful, but it will
    help us to navigate this example. 
2. Portfolio Components - on the left panel enter the symbols of the portfolio components. 
    For our example let's type SPY, ONEQ, IWM, XLK, and XLF. You have to enter one symbol name per cell. 
    It doesn't matter in what order, lower or upper case, or in what specific cell. Then press 
    `Refresh` button. The symbols will be enumerated in alphabetical order, upper case, from left to right and
    up to down. Also, entries with special characters that cannot be present in a valid
    symbol name will be eliminated silently. This is a good time to check the spelling too. 
    In our case, the 5 symbols belong to 5 very popular ETF's. However, to make sure 
    that they are valid market symbols for our market data provider, let's press on the 
    `Validate` button. A `Symbols Validation` window will popup. 

    ![alt text](panels/SymbolsValidation_panel.png)

    We will discuss later the 
    optional entries in this window. For now just notice that the market data provider 
    is `yahoo`. It is our default choice (it is free "as is"). Later, we will discuss 
    how other (pay for) market data provider can be setup. Let's press on the `Validate` 
    button. You will notice two thinks.
    * It toke a while to release the window. This is the time spent by `azapyGUI` to 
    contact the market data prover (in our case `yahoo`) and to make a minimal request for 1 (most recent) 
    historical record for each of the symbols. In this way it establish that these
    symbols are valid market shares symbols and they can be used in defining our portfolio.
    * The right side of application main panel, `Active Market Data` was populated with our symbols
    (although the length of the historical data is only 1 day - hardly enough for any computation). 
3. Optimization Model - although there are many and some of them very complex choices, for this 
    example we will make a simple choices. On the third drop-down list under the label `Optimization Model:` 
    click on `mMAD` (mixture Mean Absolute Deviation). An mMAD edit model parameter window will popup.

![alt text](panels/mMAD_model_panel.png)

We will comment later on the meaning of these parameters. For now we will accept the default values. 
They stand for maximization of Sharpe ratio with 0 risk free rate and (1,1)-mMAD risk measure, targeting 
quarterly rates of return for a look-back period of 1.25 years, using the `ecos` numerical 
library for LP (linear programming) problems. Let's press on the `Save` button. The model parameter
window will close and our model will appear in the right panel of `Portfolio Edit` window. By pressing 
on + it can be extended to view the value of all parameters. 

At this point we are almost done. What is left is to press on the `Set` button. 
The `Portfolio Edit` window will close and our model will be visible in the left panel of 
main application window. It will have 
- `Status`::`Set` - it means that the portfolio is ready for computations.
- `Save`::`False` - it means that the portfolio is not yet saved.
To save the portfolio, right click the mouse on the portfolio name. From the dropdown menu 
chose `Save` item and proceed to save the portfolio structure to a file in the default directory.

## Backtesting ##

Now we are ready to put our portfolio to the test, *i.e.*, backtest.

Right click the mouse on the portfolio name, and from the dropdown menu choose the `Backtest` item.
The `Backtesting` window will popup. 

![alt text](panels/Backtesting_panel.png)

We will accept the default values. Later we will discuss in detail all available options. 
However, it is worth mentioning a few features now. The name of our portfolio is at the top
of the screen. In general, `azapyGUI` allows for simultaneous multiple portfolio backtesting. 
In this case the the list of portfolio names will be visible at the top of
the window. End date is set to `today` (*i.e.*, most recent market closing date) and the 
start date is set to `1/1/2012` (*i.e.*, the first market closing date after, and including, 
`1/1/2012`). The rebalancing date is set 3 business days before (this is the meaning of 
`-3` value for `Bday offset` field) the end of the calendaristic quarter (the quarterly reset 
was defined by the model parameter, *i.e.*, `Q` choice for `freq` value). The fixing date
(*i.e.*, the closing day relative to witch the portfolio weights are computed) is defined 
as the closing day before the rebalancing day (*i.e.*, the `-1` value for `Fixing offset` field).
A check of `Nr Shares int` box, stands for using whole numbers (opposed to fractional)
of shares (therefore the portfolio will be subject to rebalancing round off errors - in practice they
are very small).

Let's press the start button. The backtesting process starts collecting the market data. It will take
a bit of time to retrieve the data directly from the provider and a lot faster if it is already 
cached. Then the actual numerical computations will proceed (by default `azapyGUI` will use all CPU cores available). 
The effective user time for these process (market data collection and actual numerical 
evaluations) will be posted at bottom of the window. When all the computations are done the 
`Statistics` window will popup. 

![alt text](panels/Statistics_panel.png)

The plot is our portfolio performance over time, assuming full reinvestment. On the right side 
panel there are many graphical and analytical options (numerical reports). They will be discussed later. 
For now let us look at the `Specific` section (*i.e.*, portfolio specific analytic reports) and
from the second dropdown entry click on `Annual` (*i.e.*, the annual returns report). 
The `Annual Report` window will popup.

![alt text](panels/AnnualReport_panel.png)

The portfolio and its components annual returns (percent) are presented. The negative returns are in red.
Note that, pressing the `year` heading cell, the results will be printed in descendent order of years.
To save this report, press on the menu `save` and choose the format. You will be
prompt to save the report in the default location (defined in Setting `Data Output Directory`).

We will stop this presentation here, hopping that you got a general idea about `azapyGUI` backtesting capabilities. 
Later, we will explore the full set of analytic reports.

## Rebalancing ##

Another important `azapyGUI` functionality is the computation of weights and the size of buy/sale orders 
to rebalance an exiting portfolio. 

Let's imagine that we are after today closing and tomorrow we would like to initiate a position in
`Port-MAD`. We will need to compute the weights and the number of shares that we need to buy. 
To initiate this computations, let's go back to the main panel, right click the mouse on the portfolio 
name, and select `Rebalance` item. The `Rebalance` window will popup.

![alt text](panels/Rebalance_panel.png)

In the left panel are the components of our capital. Since this is a new position on this portfolio, we will
start with a cash amount of money and zero shares. By default, in the `Cash` entry it is printed 100000 (dollars). 
You can change this value to an actual amount of dollars you want to allocate to this investment. 
Then, if you press the `Weights` button, `azapyGUI` will return a report showing the value of the weights 
for each portfolio component. This is a useful information to understand the capital allocation. 
Further, if we press on the `Treading Sheet` button, the transactions report will popup. 
Here are listed the initial, final, and delta (final-initial) positions for all assets with non zero allocations. 
This report can be saved and used next day (rebalancing day) to assist the execute of the 
actual transactions.

The similar computation for an existing portfolio requires to enter the initial (existing) number of 
shares for each portfolio component and a non-zero value for `Cash` only if we want to increase the 
capital (a positive amount) or reduce the capital (a negative value) for this strategy. Then, the `Treading Sheet` will
show the right amount of shares (delta position) that will rebalance the portfolio. 

## Backtesting Multiple Portfolios ##



## Example of a complex portfolio ##



