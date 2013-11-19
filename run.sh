python TreeRebuilder.py Data/all_0.9.gv
cd Data
sfdp -Gsmoothing=triangle -Gsize=10 all_0.9.gv_simple > 09_simple.gv
gvpr -c 'N{double x, y; sscanf($.pos, "%f,%f", &x, &y); $.pos = sprintf("%f,%f", 10*x, 10*y);}' 09_simple.gv | neato -n -Tps -Gsize=10! > 09_simple_10.ps
