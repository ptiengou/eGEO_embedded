# eGEO_embedded
This is the code I developped to use an eGEO smart meter during my internship at EnergEIA in Colombia. 
It is meant to grab measurements (voltage, current, active or reactive power, and more) from the smart meter, store them on the chip of the device (Omega Onion), and send them on a cloud server (hosted by ThingsBoard in my case).
The code contains three modules, one for each of these functionalities, and a main.py script that is the one ran to collect data.

List of Python modules necessary for the code: paho-mqtt, json, time, datetime, serial, sqlite3.
I runned the code with Python 3.7.1 on my PC and 3.6 on the Omega chip.

Note: 
I am aware that sometimes conventions are not respected or even consistent, as I was still in the process of learning object-oriented programming with Python when working on this project. I tried to do my best, but there are some common "good habits" that I may have discovered only during the project. 
Some aspects of the code are also not optimal, in particular, it is not that straight-forward to change the variables that we want the smart meter to collect and store.
