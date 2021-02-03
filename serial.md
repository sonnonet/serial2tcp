# 시리얼통신 (Tx,Rx)
  - 라즈베리파이 설정
  ```
  sudo vim /boot/config.txt
  ```
  ```
  dtoverlay=pi3-disable-bt
  ```
  ```
  sudo systemctl disable hciuart
  reboot
  ```
  - baud 확인 및 설정
  ```
  stty -F /dev/ttyAMA0(포트) 
  stty -F /dev/ttyAMA0(포트) 115200
  ```
  
