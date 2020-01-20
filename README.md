
## Remote access

```
wget https://www.vpn.net/installers/logmein-hamachi_2.1.0.203-1_armhf.deb
dpkg -i logmein-hamachi_2.1.0.203-1_armhf.deb  
sudo hamachi login
sudo hamachi attach EMAIL

/etc/init.d/logmein-hamachi start


## Install tornado
sudo apt install python3-tornado
