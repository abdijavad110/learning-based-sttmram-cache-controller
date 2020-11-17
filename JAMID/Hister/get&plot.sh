rm -rf log_L2_core-0.log
sshpass -p "1" scp sniper@172.16.3.128:/home/sniper/Desktop/sniper-mem/test/motion_blobdetection_antonio/log_L2_core-0.log .
python3 plt.py
