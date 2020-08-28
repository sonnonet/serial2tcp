# Serial 설정
  1. 블루투스 정지
  ```
    sudo vim /boot/config.txt
  ```
  ```
    #bt disabled
    dtoverlay=pi3-disable-bt
  ```
  ```
    sudo systemctl disable hciuart
  ```
  ```
    sudo reboot -h
  ```
  
