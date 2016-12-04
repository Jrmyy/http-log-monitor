HTTP Log monitoring system
==========================

Subject
-------

-   Create a simple console program that monitors HTTP traffic on your machine
-   Consume an actively written-to w3c-formatted HTTP access log
-   Every 10s, display in the console the sections of the web site with the most hits (a section is defined as being what’s before the second ‘/’ in a URL. i.e. the section for “<http://my.site.com/pages/create>’ is”<http://my.site.com/pages>“), as well as interesting summary statistics on the traffic as a whole.
-   Make sure a user can keep the console app running and monitor traffic on their machine
-   Whenever total traffic for the past 2 minutes exceeds a certain number on average, add a message saying that “High traffic generated an alert - hits = {value}, triggered at {time}”
-   Whenever the total traffic drops again below that value on average for the past 2 minutes, add another message detailing when the alert recovered
-   Make sure all messages showing when alerting thresholds are crossed remain visible on the page for historical reasons.

Project structure
-----------------

The project follows this concept:

-   First, a ConfigLoader will create the different threads by reading the config file
-   A Reader that reads each line of the log file, parses the lines and creates a dictionary thanks to the data extracted from the line, and then puts the data in a queue shared with a Displayer in order to print the stats. The Reader also shares a queue with the AlertSystem, containing the datetime of each line of the log file
-   A Displayer that displays the statistics each 10 seconds, by reading the queue shared with the reader and print the alert raising and recovering messages by getting the informations from a dictionary shared with the AlertSystem
-   An AlertSystem that checks if an alert message should be raised by getting the elements from the queue shared with the Reader, and keeping only the elements that are separated from the current time by a maximum of 2 minutes.
-   An optional LogSimulator, that writes W3C-formatted lines in a log file

Each process is running in a different thread to enable to in the log file, to read the same log file, to display the stats and the alert messages, and to check if an alert message should be raised.

How to use it ?
---------------

### Using the simulation

In order to see the algorithm works, you just need to go in the project folder, and launch the short\_simulation file. This sample is running during 3 minutes with a Reader, a Displayer, an AlertSystem and a LogSimulator. During two minutes, the LogSimulator is running to enable the raising of an alert by putting a lower threshold than the real number of requests per second. Then, for the last minute, we just stop the LogSimulator to enable the number of requests per second to drop below the threshold and to display an alert recovery message.

### Using on your own system

To perform the monitoring of your own system, you will have to use the main file. But you can custom the system with the config.ini file