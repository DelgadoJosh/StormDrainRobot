
From https://www.youtube.com/watch?v=8YKAtpPSEOk

sudo apt-get install python3-pip
sudo pip3 install adafruit-circuitpython-servokit


sudo usermod -aG i2c pjm
sudo groupadd -f -r gpio

sudo cp /opt/nvidia/jetson-gpio/etc/99-gpio.rules /etc/udev/rules.d/

sudo udevadm control --reload-rules && sudo udevadm trigger

sudo reboot now
