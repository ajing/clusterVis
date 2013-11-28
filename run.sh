python TreeRebuilder.py Data/all_0.9.gv
cd Data
sfdp -Gsmoothing=triangle -Gsize=10 all_0.9.gv_simple > 09_simple.gv
gvpr -c 'N{double x, y; sscanf($.pos, "%f,%f", &x, &y); $.pos = sprintf("%f,%f", 10*x, 10*y);}' 09_simple.gv | neato -n -Tps -Gsize=10! > 09_simple_10.ps
ps2pdf -dDEVICEWIDTHPOINTS=900 -dDEVICEHEIGHTPOINTS=679 09_simple_10.ps test.pdf

# for legend
sfdp -Gsize=10 legend.gv > legend_sf.gv
#dot -Tps legend_sf.gv > legend.ps
gvpr -c 'N{double x, y; sscanf($.pos, "%f,%f", &x, &y); $.pos = sprintf("%f,%f", 10*x, 10*y);}' legend_sf.gv | dot -Tps -Gsize=10! > legend.ps
ps2pdf -dDEVICEWIDTHPOINTS=400 -dDEVICEHEIGHTPOINTS=400 legend.ps legend.pdf
