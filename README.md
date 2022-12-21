# doggyhearts

Basic example how to start writing Android games in Python. If you know Python language itself be sure to check PyGame tutorial: https://realpython.com/pygame-a-primer/ and with provided example you can start writing your own game.

Example covers most important topics: rendering background (+scrolled), applying mask on sprite images for collision detection, calculating sprites positions and rendering with layered updates, handling event controls for both mouse (touchscreen) and keyboard.

Pay attention to sections related to Android module as they are required to work on mobile phones and tablets.

Install PyGame (on Debian/Ubuntu: <code>sudo apt install python3-pygame</code>) and just clone <code>git clone https://github.com/zygtech/doggyhearts</code> and run Python script with <code>python3 main.py</code>.

Python code is Android ready just follow instructions on https://github.com/startgridsrc/pgs4a to deploy it for mobiles:

- install Java 8 from: https://bell-sw.com/pages/downloads/#/java-8-lts
- install Python2.7 and PyGame for Python2.7: <code>sudo apt install python2.7</code> <code>wget https://bootstrap.pypa.io/pip/2.7/get-pip.py</code> <code>python2.7 get-pip.py</code> <code>python2.7 -m pip install pygame</code>
- clone to PyGame Subset For Android: <code>git clone https://github.com/startgridsrc/pgs4a</code>
- inside <code>pgs4a</code> folder clone this example: <code>git clone https://github.com/zygtech/doggyhearts</code>
- install SDK: <code>python2.7 ./android.py installsdk</code>
- configure game: <code>python2.7 ./android.py configure doggyhearts</code>
- and finally deploy: <code>python2.7 ./android.py build doggyhearts release install</code>
