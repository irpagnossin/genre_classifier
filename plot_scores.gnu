set datafile separator ","
set key autotitle columnhead
set autoscale
set xlabel "# of genres"
set ylabel "silhouette score"
plot 'output/200/silhouette.csv' with linespoints linestyle 7 lt 2 title 'f >= 200', 'output/900/silhouette.csv' with linespoints linestyle 7 lt 1 title 'f >= 900'
pause -1