set myport=com9
ampy --port %myport% put mkdir.py ./
ampy --port %myport% run --no-output mkdir.py
ampy --port %myport% put lib/SRV/sword_srv/SWORD.py lib/SRV/sword_srv/SWORD.py
ampy --port %myport% put lib/SRV/car_srv/Car.py lib/SRV/car_srv/Car.py
ampy --port %myport% put lib/DRV/GYRO/MPU6050_JY61P.py lib/DRV/GYRO/MPU6050_JY61P.py
ampy --port %myport% put lib/DRV/SENSOR/HCSR04.py lib/DRV/SENSOR/HCSR04.py
ampy --port %myport% put lib/DRV/SERVO/DRV8833.py lib/DRV/SERVO/DRV8833.py
ampy --port %myport% put lib/DRV/SERVO/MD_L298N.py lib/DRV/SERVO/MD_L298N.py
ampy --port %myport% put lib/DRV/SERVO/MD_TB6612FNG.py lib/DRV/SERVO/MD_TB6612FNG.py
ampy --port %myport% put lib/DRV/SERVO/servo_MG996R.py lib/DRV/SERVO/servo_MG996R.py
ampy --port %myport% put lib/COMMON/Arduino.py lib/COMMON/Arduino.py
ampy --port %myport% put lib/COMMON/force.py lib/COMMON/force.py
ampy --port %myport% put lib/COMMON/management.py lib/COMMON/management.py
ampy --port %myport% put lib/COMMON/MMG_server.py lib/COMMON/MMG_server.py
ampy --port %myport% put lib/COMMON/MMG_client.py lib/COMMON/MMG_client.py
ampy --port %myport% put lib/COMMON/timer.py lib/COMMON/timer.py
ampy --port %myport% put lib/CLI/gyroctrl_cli/GYROCTRL.py lib/CLI/gyroctrl_cli/GYROCTRL.py
ampy --port %myport% put lib/CLI/switch_cli/SWITCH.py lib/CLI/switch_cli/SWITCH.py

