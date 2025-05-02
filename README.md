# TRG Week 22

## Stock Analysis

- Link To Dataset : https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs

### 1st Commit

- Selected MSFT for weekly analysis. Loaded msft.us.txt to an HTML dataframe within data.py for cleaning & preparation.

### 2nd Commit

- Clean data by dropping the "OpenInt" column. and drop all rows dated before January 1st, 2000.

### 3rd Commit

- Generate a plot chart through a new route to show the monthly aggregate low price for all rows dated for the year of 2017. Make the Y-axis represent the price, and the X-axis for the months. Use the columns "Low" & "Date". Make the plotted line solid green.

- Add another line to the same chart and route, but showing the moonthly aggregate high price for the year of 2017. Use the "High" attribute and make the line solid red.

### 4th Commit

- To the same chart as before, add the monthly aggregate line plots for the High and Low prices of the year 2007. While keeping the original /plot code the same, make the 2007 "Low" attribute line dashed green, and the 2007 "High" attribute line dashed red.

- The code is correct, but I want all four lines oriented along the same 12 months on the X-axis.

- There is an error in the data. It is showing all years between 2007 and 2017. I want to load only the rows dated for the years 2007 and 2017.

- Data Error Fixed.

- Created two routes /plot_2017 & /plot_2007 to fix the issue and visualize the proces more effectively.

### 5th Commit

- Using the High and Low prices for 2007 & 2017, generate a third route which shows a predicted monthly median price for the year of 2027.

- The visual plots a very negative downtrend. This is biased, the price movement is based on 2 years of numerical data with no other influence. Maybe calculating price movement in sets of 5 years will yield better results.