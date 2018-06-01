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
        

def runcommands(cs, ts, ss, verbose = False):
    """ Runs a series of commands at certain specified times """
    if len(ts) == len(cs):
        i = 0
        t0 = time.time()
        dt = time.time() - t0 # elapsed time
        while i < len(cs):
            while (dt - ts[i]) < 0.0005:
                dt = time.time() - t0
                if verbose: read_and_print(ss[i])
#            if verbose: print("Time: {:2.3f}".format(dt))
            write_command(ss[i], cs[i], verbose)
            i += 1
    else:
        print('Error: Lists are not equally long. ')




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
      1.080]

ps = ["COM1",
      "COM1",
      "COM1",
      "COM1",
      "COM1"]

ports = list(set(ps))

slave = False

reps = 2
cs_rep = cs*reps
ts_rep = []
for r in range(reps):
    for t in ts:
        ts_rep.append(t + ts[-1]*r)


runcommands(ser, cs_rep, ts_rep, verbose=True)
    
time.sleep(0.5)
ser.close()