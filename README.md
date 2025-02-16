ASSETTO CORSA QUAD-14-SEGMENT DIISPLAY TACOMETER

https://github.com/user-attachments/assets/3dae7164-1e6b-4f3e-9a35-dd4791cce64a

Default display configuration is set for 100hz refresh
Top display is speed in Kph and Mph
Bottom display is gear and rpm

There are two portions of this codebase
  1. an assetto corsa mod called 'metering'
  2. circuitpython for rp2040 microcontroller
      (specifically this https://www.waveshare.com/rp2040-zero.htm,
       but others should work...)
For my 14-segment displays I used these EC Digital Tube Module 0.54 Inch 4 digit
(https://www.amazon.com/EC-Buying-Digital-Display-Segment/dp/B0BXDL1LFT?th=1)
For use with the adafruit ht16k33 circuitpython library (included in repo)

INSTRUCTIONS
Assetto Corsa:
Install the Assetto Corsa mod as a 'Python App' and configure the com.cfg
to whatever COM port is being used for your rp2040 serial device

RP2040 Microcontroller:
Configure the i2c hardware definitions accordingly to your
build of the hardware, then drag and drop the code directly
onto the rp2040 flash storage (including lib folder)

Pictures are included to see how I have wired my boards:
![20250215_213650](https://github.com/user-attachments/assets/c5da1eca-1c09-4a60-a535-1fd2f9abce24)
![20250215_213657](https://github.com/user-attachments/assets/5eae11de-fec8-4315-979f-f47f98bc673d)

