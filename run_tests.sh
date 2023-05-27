#! /bin/sh
python3.10 test.py tests/testgraphs/testgraph_1.txt tests/results/result1.txt
echo "#1 done"
python3.10 test.py tests/testgraphs/testgraph_2.txt tests/results/result2.txt
echo "#2 done"
python3.10 test.py tests/testgraphs/testgraph_3.txt tests/results/result3.txt
echo "#3 done"
python3.10 test.py tests/testgraphs/testgraph_4.txt tests/results/result4.txt
echo "#4 done"
python3.10 test.py tests/testgraphs/testgraph_5.txt tests/results/result5.txt
echo "#5 done"
python3.10 test.py tests/testgraphs/testgraph_6.txt tests/results/result6.txt
echo "#6 done"
python3.10 test.py tests/testgraphs/socfb-Middlebury45.txt tests/results/result8.txt
echo "#8 done"
python3.10 test.py tests/testgraphs/socfb-Reed98.txt tests/results/result9.txt
echo "#9 done"
python3.10 test.py tests/testgraphs/team_6.txt tests/results/result10.txt
echo "#10 done"

