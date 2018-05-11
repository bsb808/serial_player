#!/usr/bin/python

'''
serialplay.py
Utility for sending strings to a serial port.
Reads lines from a file and transmits them on the given serial port.
Useful for developing serial device/sensor drivers.

USAGE
>> ./serialplay.py [OPTIONS]

OPTIONS
-h        Print help
-p PORT   Set the serial transmit to the PORT (e.g., /dev/ttyS1)
          Default = /dev/ttyUSB1
-b BAUD   Set the serial transmit to baud rate of BAUD (e.g., 9600)
          Default = 9600
-s SLP    Set the inter-string transmit delay to SLP seconds (float)
          Default = 1.0 seconds
-f FNAME  Read the strings from the file FNAME
          Default = serialplay.txt

'''

import serial, sys, time, math, getopt

def usage():
    print __doc__

def main(argv):
    # Defaults
    txPort = '/dev/ttyUSB1'
    txBaudRate = 9600
    fname = 'serialplay.txt'
    sleepsec = 1.0
    
    # Process command line options
    try:                                
        opts, args = getopt.getopt(argv, "hf:p:b:s:", []) 
    except getopt.GetoptError:           
        print "For help use -h"
        usage()
        sys.exit(2)
    for opt, arg in opts:
        print opt
        print arg
        if opt == '-h':
            usage()
            sys.exit(2)
        if opt == '-f':
            fname = arg
        if opt == '-p':
            txPort = arg
        if opt == '-b':
            txBaudRate = int(arg)
        if opt == '-s':
            sleepsec = float(arg)
            
    # Open the TX serial port
    print("Opening serial port on <%s>"%txPort)
    #txSer = serial.Serial(txPort,txBaudRate)
    # Do this for socat virtual ports
    txSer = serial.Serial(txPort,txBaudRate,rtscts=True,dsrdtr=True)
    print "\nOpened serial port for tranmit:", txSer

    # Report the sleep setting
    print "Inter-string sleep is %f seconds"%sleepsec
    
    # Open file for strings to transmit
    while(True):
        print "\nOpening file <%s> for echoing to serial port"%fname
        
        try:
            f = open(fname,'r')
        except IOError:
            print "Couldn't open the file!"
            print sys.exc_info()[0]
            sys.exit()
            
        for line in f:
            print("TX:%s"%line)
            txSer.write(line)
            time.sleep(sleepsec)
            
        f.close()

    txSer.close()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print "Exitting..."
    
