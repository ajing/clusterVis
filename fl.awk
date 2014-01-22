# usage: sed 's/\t\t*/ /g' 09_simple.gv_test | awk -f ../fl.awk
{
  if ($0 ~ /\[/) {in_attr=1; printf("%s",$0);}
  else if ($0 ~ /\]/) {in_attr=0; printf("%s\n",$0);}
  else if (in_attr) printf("%s",$0);
  else print $0;
}
