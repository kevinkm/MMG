#HOWTO replace SWORD.py
# 1. upload SWORD.py
# 2. Run the codes in webrepl
os.remove('./lib/SRV/sword_srv/SWORD.py')
os.rename('SWORD.py', './lib/SRV/sword_srv/SWORD.py' )
os.rename('force.py', './lib/COMMON/force.py' )

./lib/DRV/GYRO/MPU6050_JY61P.py
./lib/COMMON/MMG_client.py

os.listdir('./lib/COMMON')
os.listdir('./lib/CLI/gyroctrl_cli')
os.listdir('./lib/CLI/switch_cli')


exec(open('./gyroCTRLcar.py').read(),globals())