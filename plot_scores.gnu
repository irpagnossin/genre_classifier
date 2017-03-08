set datafile separator ","
set key autotitle columnhead
set autoscale
plot 'output/silhouette_900.csv' with linespoints linestyle 7, 'output/silhouette_800.csv' with linespoints linestyle 7 lt rgb "green", 'output/silhouette_700.csv' with linespoints linestyle 7 lt rgb "green", 'output/silhouette_600.csv' with linespoints linestyle 7 lt rgb "green", 'output/silhouette_500.csv' with linespoints linestyle 7 lt rgb "green", 'output/silhouette_400.csv' with linespoints linestyle 7 lt rgb "green", 'output/silhouette_300.csv' with linespoints linestyle 7 lt rgb "green", 'output/silhouette_200.csv' with linespoints linestyle 7 lt rgb "green"
pause -1
