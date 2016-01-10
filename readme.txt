command for using parquetreader.py:


/opt/spark/bin/spark-submit  --master local[15] /var/home/root/shubham.py --file /data/collector/1/output/tektronicswireless/2015/12/10/16/30 --out /var/home/root/final23.txt --col 1,2,3,4,5,6,7,8,9,10


command for using header_getter.py

/opt/spark/bin/spark-submit  --master local[15] /var/home/root/header.py --file /data/collector/1/output/scefixed/2015/12/10/16/30
