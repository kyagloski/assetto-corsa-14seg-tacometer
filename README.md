ASSETTO CORSA QUAD-14-SEGMENT DISPLAY TACOMETER<br/>

https://github.com/user-attachments/assets/3dae7164-1e6b-4f3e-9a35-dd4791cce64a<br/>

Default display configuration is set for 100hz refresh <br/>
Top display is speed in Kph and Mph<br/>
Bottom display is gear and rpm<br/>

There are two portions of this codebase<br/>
  1. an assetto corsa mod called 'metering'<br/>
  2. circuitpython for rp2040 microcontroller<br/>
      (specifically this https://www.waveshare.com/rp2040-zero.htm,<br/>
       but others should work...)<br/>
For my 14-segment displays I used these EC Digital Tube Module 0.54 Inch 4 digit<br/>
(https://www.amazon.com/EC-Buying-Digital-Display-Segment/dp/B0BXDL1LFT?th=1)<br/>
For use with the adafruit ht16k33 circuitpython library (included in repo)<br/>

INSTRUCTIONS<br/>
Assetto Corsa:<br/>
Install the Assetto Corsa mod as a 'Python App' and configure the com.cfg<br/>
to whatever COM port is being used for your rp2040 serial device<br/>

RP2040 Microcontroller:<br/>
Configure the i2c hardware definitions accordingly to your<br/>
build of the hardware, then drag and drop the code directly<br/>
onto the rp2040 flash storage (including lib folder)<br/>

Pictures are included to see how I have wired my boards:<br/>
![20250215_213650](https://github.com/user-attachments/assets/c5da1eca-1c09-4a60-a535-1fd2f9abce24)<br/>
![20250215_213657](https://github.com/user-attachments/assets/5eae11de-fec8-4315-979f-f47f98bc673d)<br/>

