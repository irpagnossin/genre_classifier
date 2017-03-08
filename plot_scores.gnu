set datafile separator ","
set key autotitle columnhead
set autoscale
plot 'silhouette_950.csv' with linespoints linestyle 7
pause -1