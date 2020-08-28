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
  2. USB 연결 확인
  ```
    ls /dev/tty 
  ```
  
  
  ## 문자열 Parsing
  ```
   <REG>"현재값"<INIT>"초기값"<MAX>"최대값"  // 단위 K
  ```
    ```
      ser = serial/Serial('dev'ttyACM0', 9600, timeout = 5)
      rcvBuf = bytearray()
      ser.reset_input_buffer()
      rcvBuf = ser.read_until(size=40)
      
      rcvBuf[rcvBuf.find('G')+2:rcvBuf.find('I')-1]
      rcvBuf[rcvBuf.find('T')+2:rcvBuf.find('M')-1]
      rcvBuf[rcvBuf.find('X')+2:len(rcvBuf)-1]
    ```
