import os

cmd = "sshpass -p bits2018 scp ar_migrate_test.tar HDUSER@172.18.16.47:/home/HDUSER"
os.system(cmd)