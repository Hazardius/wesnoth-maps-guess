wesnoth-mapgen
========================
Hopfield network used for prediction of Battle for Wesnoth map tiles in randomly generated maps.

Requirements:
-------------
* [__numpy__](http://www.numpy.org/)

---

Input.
-------
  One file from patterns as a source of patterns and one file from tests as a source of tests.

Output.
-------
  Default output file is named `results.txt`. It contains results of predictions made by naural network created in previous session of running this script.

Usage:
------
  To run a map generator use this command with different options. 
  
  For beginning try asking for help:

        python __init__.py -h
