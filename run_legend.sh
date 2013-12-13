cd Data
sfdp -Gsize=10 legend.gv > legend_sf.gv
#dot -Tps legend_sf.gv > legend.ps
gvpr -c 'N{double x, y; sscanf($.pos, "%f,%f", &x, &y); $.pos = sprintf("%f,%f", 10*x, 10*y);}' legend_sf.gv | dot -Tps > legend.ps
ps2pdf -dDEVICEWIDTHPOINTS=400 -dDEVICEHEIGHTPOINTS=400 legend.ps test.pdf
