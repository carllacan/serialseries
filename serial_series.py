# -*- coding: utf-8 -*-

import serial
import time

     
def write_command(serial, comm, verbose = False):
    """ Encodes a command and sends it over the serial port """
    if verbose and comm != "":
        print(comm)
#   serial.write(comm.encode())
            
    
def read_buffer(serial):
    """ Reads the serial port bufer and decodes it """
    resp = serial.read_all()
    return resp.decode()

def read_and_print(serial):
    """ Obtains serial responser and prints it if it's not empty """
    resp = read_buffer(serial)
    if resp != "":
        print(resp)
        

def runcommands(serial, cs, ts, verbose = False):
    """ Runs a series of commands at certain specified times """
    if len(ts) == len(cs):
        i = 0
        t0 = time.time()
        dt = time.time() - t0 # elapsed time
        while i < len(cs):
            while (dt - ts[i]) < 0.0005:
                dt = time.time() - t0
                if verbose: read_and_print(serial)
#            if verbose: print("Time: {:2.3f}".format(dt))
            write_command(serial, cs[i], verbose)
            i += 1
    else:
        print('Error: Times and commands lists are not equally long. ')




port = "COM1"
baudrate = 38400

ser = serial.Serial(port = port, 
                    baudrate=baudrate,
                    write_timeout=0,
                    bytesize=serial.EIGHTBITS,
                    stopbits=serial.STOPBITS_ONE,
                    parity=serial.PARITY_NONE)

cs = ["F", # PRE
      "L", # CH
      "F", # PRE
      "L", # CH
      ""]

ts = [0.000,
      0.040,
      0.080,
      1.040,
      6.080]



#cs = ["F", 
#      "L",
#      "F",
#      "L",
#      ""]
#
#ts = [0.000,
#      0.040,
#      0.080,
#      0.100,
#      1.000]

slave = False

reps = 2
cs_rep = cs*reps
ts_rep = []
for r in range(reps):
    for t in ts:
        ts_rep.append(t + ts[-1]*r)

if slave: write_command(ser, "m", verbose=True)
#time.sleep(0.1)
#ftn.read_print()

#for i in range(reps):
#    ftn.runcommands(cs, ts)
runcommands(ser, cs_rep, ts_rep, verbose=True)
    
time.sleep(0.5)
if slave: write_command(ser, "m", verbose=True)
time.sleep(0.5)
ser.close()