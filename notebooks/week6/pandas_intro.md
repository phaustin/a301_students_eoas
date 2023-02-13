---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

<center><img src="https://github.com/pandas-dev/pandas/raw/main/web/pandas/static/img/pandas.svg" alt="pandas Logo" style="width: 800px;"/></center>

(week6:pandas_intro)=
# Introduction to Pandas

The notebook is copied from [Project Pythia](https://foundations.projectpythia.org/core/pandas.html).  The source code is [here](https://github.com/ProjectPythia/pythia-foundations/tree/main/core/pandas)
---

+++

## Overview
1. Introduction to pandas data structures
1. How to slice and dice pandas dataframes and dataseries
1. How to use pandas for exploratory data analysis

## Prerequisites

| Concepts | Importance | Notes |
| --- | --- | --- |
| [Python Quickstart](../../foundations/quickstart) | Necessary | Intro to `dict` |
| [Numpy Basics](../numpy/numpy-basics) | Necessary | |

* **Time to learn**: 60 minutes

+++

---

+++

## Imports

+++

You will often see the nickname `pd` used as an abbreviation for pandas in the import statement, just like `numpy` is often imported as `np`. Here we will also be importing `pythia_datasets`, our tool for accessing example data we provide for our materials.

```{code-cell} ipython3
import pandas as pd
from pythia_datasets import DATASETS
```

## The pandas [`DataFrame`](https://pandas.pydata.org/docs/user_guide/dsintro.html#dataframe)...
... is a **labeled**, two dimensional columnal structure similar to a table, spreadsheet, or the R `data.frame`.

![dataframe schematic](https://github.com/pandas-dev/pandas/raw/main/doc/source/_static/schemas/01_table_dataframe.svg "Schematic of a pandas DataFrame")

The `columns` that make up our `DataFrame` can be lists, dictionaries, NumPy arrays, pandas `Series`, or more. Within these `columns` our data can be any texts, numbers, dates and times, or many other data types you may have encountered in Python and NumPy. Shown here on the left in dark gray, our very first `column`  is uniquely referrred to as an `Index`, and this contains information characterizing each row of our `DataFrame`. Similar to any other `column`, the `index` can label our rows by text, numbers, `datetime`s (a popular one!), or more.

Let's take a look by reading in some `.csv` data, which comes from the NCDC teleconnections database, including various El Niño Southern Oscillation (ENSO) indices! [[ref](https://www.ncdc.noaa.gov/teleconnections/enso/indicators/sst/)].

+++

<div class="admonition alert alert-info">
    <p class="admonition-title" style="font-weight:bold">Info</p>
    Here we're getting the data from Project Pythia's custom library of example data, which we already imported above with <code>from pythia_datasets import DATASETS</code>. The <code>DATASETS.fetch()</code> method will automatically download and cache our example data file <code>enso_data.csv</code> locally.
</div>

```{code-cell} ipython3
filepath = DATASETS.fetch('enso_data.csv')
```

Once we have a valid path to a data file that Pandas knows how to read, we can open it like this:

```{code-cell} ipython3
df = pd.read_csv(filepath)
```

If we print out our dataframe, you will notice that is text based, which is okay, but not the "best" looking output

```{code-cell} ipython3
print(df)
```

Instead, if we just use the pandas dataframe itself (without wrapping it in `print`), we have a nicely rendered table which is native to pandas and Jupyter Notebooks. See how much nicer that looks?

```{code-cell} ipython3
df
```

The `index` within pandas is essentially a list of the unique row IDs, which by default, is a list of sequential integers which start at 0

```{code-cell} ipython3
df.index
```

Our indexing column isn't particularly helpful currently. Pandas is clever! A few optional keyword arguments later, and...

```{code-cell} ipython3
df = pd.read_csv(filepath, index_col=0, parse_dates=True)

df
```

```{code-cell} ipython3
df.index
```

... now we have our data helpfully organized by a proper `datetime`-like object. Each of our multiple columns of data can now be referenced by their date! This sneak preview at the pandas `DatetimeIndex` also unlocks for us much of pandas most useful time series functionality. Don't worry, we'll get there. What are the actual columns of data we've read in here?

```{code-cell} ipython3
df.columns
```

## The pandas [`Series`](https://pandas.pydata.org/docs/user_guide/dsintro.html#series)...

... is essentially any one of the columns of our `DataFrame`, with its accompanying `Index` to provide a label for each value in our column.

![pandas Series](https://github.com/pandas-dev/pandas/raw/main/doc/source/_static/schemas/01_table_series.svg "Schematic of a pandas Series")

The pandas `Series` is a fast and capable 1-dimensional array of nearly any data type we could want, and it can behave very similarly to a NumPy `ndarray` or a Python `dict`. You can take a look at any of the `Series` that make up your `DataFrame` with its label and the Python `dict` notation, or with dot-shorthand:

```{code-cell} ipython3
df["Nino34"]
```

<div class="alert alert-block alert-info">
<b>Tip:</b> You can also use the `.` (dot) notation, as seen below, but this is moreso a "convenience feature", which for the most part is interchangeable with the dictionary notation above, except when the column name is not a valid Python object (ex. column names beginning with a number or a space)</div>

```{code-cell} ipython3
df.Nino34
```

## Slicing and Dicing the `DataFrame` and `Series`

We will expand on what you just saw, soon! Importantly,

> **Everything in pandas can be accessed with its label**,

no matter how your data is organized.

+++

### Indexing a `Series`

Let's back up a bit here. Once more, let's pull out one `Series` from our `DataFrame` using its column label, and we'll start there.

```{code-cell} ipython3
nino34_series = df["Nino34"]

nino34_series
```

`Series` can be indexed, selected, and subset as both `ndarray`-like,

```{code-cell} ipython3
nino34_series[3]
```

and `dict`-like, using labels

```{code-cell} ipython3
nino34_series["1982-04-01"]
```

These two can be extended in ways that you might expect,

```{code-cell} ipython3
nino34_series[0:12]
```

<div class="admonition alert alert-info">
    <p class="admonition-title" style="font-weight:bold">Info</p>
    Index-based slices are <b>exclusive</b> of the final value, similar to Python's usual indexing rules.
</div>

+++

as well as potentially unexpected ways,

```{code-cell} ipython3
nino34_series["1982-01-01":"1982-12-01"]
```

That's right, label-based slicing! Pandas will do the work under the hood for you to find this range of values according to your labels.

+++

<div class="admonition alert alert-info">
    <p class="admonition-title" style="font-weight:bold">Info</p>
    label-based slices are <b>inclusive</b> of the final value, different from above!
</div>

+++

If you are familiar with [xarray](../xarray), you might also already have a comfort with creating your own `slice` objects by hand, and that works here!

```{code-cell} ipython3
nino34_series[slice("1982-01-01", "1982-12-01")]
```

### Using `.iloc` and `.loc` to index

Let's introduce pandas-preferred ways to access your data by label, `.loc`, or by index, `.iloc`. They behave similarly to the notation introduced above, but provide more speed, security, and rigor in your value selection, as well as help you avoid [chained assignment warnings](https://pandas.pydata.org/docs/user_guide/indexing.html#returning-a-view-versus-a-copy) within pandas.

```{code-cell} ipython3
nino34_series.iloc[3]
```

```{code-cell} ipython3
nino34_series.iloc[0:12]
```

```{code-cell} ipython3
nino34_series.loc["1982-04-01"]
```

```{code-cell} ipython3
nino34_series.loc["1982-01-01":"1982-12-01"]
```

### Extending to the `DataFrame`

These capabilities extend back to our original `DataFrame`, as well!

```{code-cell} ipython3
:tags: [raises-exception]

df["1982-01-01"]
```

<div class="admonition alert alert-danger">
    <p class="admonition-title" style="font-weight:bold">Danger</p>
    Or do they?
</div>

+++

They do! Importantly however, indexing a `DataFrame` can be more strict, and pandas will try not to too heavily assume what you are looking for. So, by default we can't pull out a row within `df` by its label alone, and **instead labels are for identifying columns within `df`**,

```{code-cell} ipython3
df["Nino34"]
```

and integer indexing will similarly get us nothing,

```{code-cell} ipython3
:tags: [raises-exception]

df[0]
```

Knowing now that we can pull out one of our columns as a series with its label, and using our experience interacting with the `Series` `df["Nino34"]`, we can chain our brackets to pull out any value from any of our columns in `df`.

```{code-cell} ipython3
:tags: []

df["Nino34"]["1982-04-01"]
```

```{code-cell} ipython3
df["Nino34"][3]
```

However, this is not a pandas-preferred way to index and subset our data, and has limited capabilities for us. As we touched on before, `.loc` and `.iloc` give us more to work with, and their functionality grows further for `df`.

```{code-cell} ipython3
df.loc["1982-04-01", "Nino34"]
```

<div class="admonition alert alert-info">
    <p class="admonition-title" style="font-weight:bold">Info</p>
    Note the <code>[<i>row</i>, <i>column</i>]</code> ordering!
</div>

+++

These allow us to pull out entire rows of `df`,

```{code-cell} ipython3
df.loc["1982-04-01"]
```

```{code-cell} ipython3
df.loc["1982-01-01":"1982-12-01"]
```

```{code-cell} ipython3
df.iloc[3]
```

```{code-cell} ipython3
df.iloc[0:12]
```

Even further,

```{code-cell} ipython3
df.loc[
    "1982-01-01":"1982-12-01",  # slice of rows
    ["Nino12", "Nino3", "Nino4", "Nino34"],  # list of columns
]
```

<div class="admonition alert alert-info">
    <p class="admonition-title" style="font-weight:bold">Info</p>
    For a more comprehensive explanation, which includes additional examples, limitations, and compares indexing methods between DataFrame and Series see <a href="https://pandas.pydata.org/docs/user_guide/indexing.html">pandas' rules for indexing.</a>
</div>

+++

## Exploratory Data Analysis

### Get a Quick Look at the Beginning/End of your `Dataframe`
Pandas also gives you a few shortcuts to quickly investigate entire `DataFrame`s.

```{code-cell} ipython3
df.head()
```

```{code-cell} ipython3
df.tail()
```

### Quick Plots of Your Data
A good way to explore your data is by making a simple plot. Pandas allows you to plot without even calling `matplotlib`! Here, we are interested in the `Nino34` series. Check this out...

```{code-cell} ipython3
df.Nino34.plot();
```

Before, we called `.plot()` which generated a single line plot. This is helpful, but there are other plots which can also help with understanding your data! Let's try using a histogram to understand distributions...

The only part that changes here is we are subsetting for just two `Nino` indices, and after `.plot`, we include `.hist()` which stands for histogram

```{code-cell} ipython3
df[['Nino12', 'Nino34']].plot.hist();
```

We can see some clear differences in the distributions, which is helpful! Another plot one might like to use would be a `boxplot`. Here, we replace `hist` with `box`

```{code-cell} ipython3
df[['Nino12', 'Nino34']].plot.box();
```

Here, we again see a clear difference in the distributions. These are not the only plots you can use within pandas! For more examples of plotting choices, check out [the pandas plot documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html)

+++

#### Customize your Plot
These `plot()` methods are just wrappers to matplotlib, so with a little more work the plots can be customized just like any matplotlib figure.

```{code-cell} ipython3
df.Nino34.plot(
    color='black',
    linewidth=2,
    xlabel='Year',
    ylabel='ENSO34 Index (degC)',
    figsize=(8, 6),
);
```

This can be a great way to take a quick look at your data, but what if you wanted a more ***quantitative*** perspective? We can use the `describe` method on our `DataFrame`; this returns a table of summary statistics for all columns in the `DataFrame`

### Basic Statistics

By using the `describe` method, we see some general statistics! Notice how calling this on the dataframe returns a table with all the `Series`

```{code-cell} ipython3
df.describe()
```

You can look at specific statistics too, such as mean! Notice how the output is a `Series` (column) now

```{code-cell} ipython3
df.mean()
```

If you are interested in a single column mean, subset for that and use `.mean`

```{code-cell} ipython3
df.Nino34.mean()
```

### Subsetting Using the Datetime Column

You can use techniques besides slicing to subset a `DataFrame`. Here, we provide examples of using a couple other options.

Say you only want the month of January - you can use `df.index.month` to query for which month you are interested in (in this case, 1 for the month of January)

```{code-cell} ipython3
# Uses the datetime column
df[df.index.month == 1]
```

You could even assign this month to a new column!

```{code-cell} ipython3
df['month'] = df.index.month
```

Now that it is its own column (`Series`), we can use `groupby` to group by the month, then taking the average, to determine average monthly values over the dataset

```{code-cell} ipython3
df.groupby('month').mean().plot();
```

### Investigating Extreme Values

+++

You can also use ***conditional indexing***, such that you can search where rows meet a certain criteria. In this case, we are interested in where the Nino34 anomaly is greater than 2

```{code-cell} ipython3
df[df.Nino34anom > 2]
```

You can also sort columns based on the values!

```{code-cell} ipython3
df.sort_values('Nino34anom')
```

Let's change the way that is ordered...

```{code-cell} ipython3
df.sort_values('Nino34anom', ascending=False)
```

### Resampling
Here, we are trying to resample the timeseries such that the signal does not appear as noisy. This can helpfule when working with timeseries data! In this case, we resample to a yearly average (`1Y`) instead of monthly values

```{code-cell} ipython3
df.Nino34.plot();
```

```{code-cell} ipython3
df.Nino34.resample('1Y').mean().plot();
```

### Applying operations to a dataframe

Often times, people are interested in applying calculations to data within pandas `DataFrame`s. Here, we setup a function to convert from degrees Celsius to Kelvin

```{code-cell} ipython3
def convert_degc_to_kelvin(temperature_degc):
    """
    Converts from degrees celsius to Kelvin
    """

    return temperature_degc + 273.15
```

Now, this function accepts and returns a single value

```{code-cell} ipython3
# Convert a single value
convert_degc_to_kelvin(0)
```

But what if we want to apply this to our dataframe? We can subset for Nino34, which is in degrees Celsius

```{code-cell} ipython3
nino34_series
```

Notice how the object type is a pandas series

```{code-cell} ipython3
type(df.Nino12[0:10])
```

If you call `.values`, the object type is now a numpy array. Pandas `Series` values include numpy arrays, and calling `.values` returns the series as a numpy array!

```{code-cell} ipython3
type(df.Nino12.values[0:10])
```

Let's apply this calculation to this `Series`; this returns another `Series` object.

```{code-cell} ipython3
convert_degc_to_kelvin(nino34_series)
```

If we include `.values`, it returns a `numpy array`

+++

<div class="admonition alert alert-warning">
    <p class="admonition-title" style="font-weight:bold">Warning</p>
    We don't usually recommend converting to NumPy arrays unless you need to - once you convert to NumPy arrays, the helpful label information is lost... so beware! 
</div>

```{code-cell} ipython3
convert_degc_to_kelvin(nino34_series.values)
```

We can now assign our pandas `Series` with the converted temperatures to a new column in our dataframe!

```{code-cell} ipython3
df['Nino34_degK'] = convert_degc_to_kelvin(nino34_series)
```

```{code-cell} ipython3
df.Nino34_degK
```

Now that our analysis is done, we can save our data to a `csv` for later - or share with others!

```{code-cell} ipython3
df.to_csv('nino_analyzed_output.csv')
```

```{code-cell} ipython3
pd.read_csv('nino_analyzed_output.csv', index_col=0, parse_dates=True)
```

---
## Summary
* Pandas is a very powerful tool for working with tabular (i.e. spreadsheet-style) data
* There are multiple ways of subsetting your pandas dataframe or series
* Pandas allows you to refer to subsets of data by label, which generally makes code more readable and more robust
* Pandas can be helpful for exploratory data analysis, including plotting and basic statistics
* One can apply calculations to pandas dataframes and save the output via `csv` files

### What's Next?
In the next notebook, we will look more into using pandas for more in-depth data analysis.

## Resources and References
1. [NOAA NCDC ENSO Dataset Used in this Example](https://www.ncdc.noaa.gov/teleconnections/enso/indicators/sst/)
1. [Getting Started with Pandas](https://pandas.pydata.org/docs/getting_started/index.html#getting-started)
1. [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html#user-guide)

```{code-cell} ipython3

```
