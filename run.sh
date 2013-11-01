python TreeRebuilder.py Data/all_0.9.gv
cd Data
sfdp -Gsmoothing=triangle all_0.9.gv_simple > 09_simple.gv
gvpr -c 'N{double x, y; sscanf($.pos, "%f,%f", &x, &y); $.pos = sprintf("%f,%f", 30*x, 30*y);}' 09_simple.gv | neato -n -Tps > 09.ps
