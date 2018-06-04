# -*- coding: utf-8 -*-

import serial
import time

     
def write_command(serial, comm, verbose = False):
    """ Encodes a command and sends it over the serial port """
    if verbose and comm != "":
        print(comm)
    serial.write(comm.encode())
            
def read_buffer(serial):
    """ Reads the serial port bufer and decodes it """
    resp = serial.read_all()
    return resp.decode()

def read_and_print(serial):
    """ Obtains serial responser and prints it if it's not empty """
    resp = read_buffer(serial)
    if resp != "":
        print(resp)
        

def runcommands(cs, ts, ps, serials, verbose = False):
    """ Runs a series of commands at certain specified times """
    if len(ts) == len(cs):
        i = 0
        t0 = time.time()
        dt = time.time() - t0 # elapsed time
        while i < len(cs):
            ser = serials[ps[i]]
            comm = cs[i]
            t = ts[i]
            while (dt - t) < 0.0005:
                dt = time.time() - t0
                if verbose: read_and_print(ser)
            if verbose: print("Time: {:2.3f}".format(dt))
            write_command(ser, comm, verbose)
            i += 1
    else:
        print('Error: Lists are not equally long. ')


def load_csv(fname):
    delimiter = ','
    f = open(fname, 'r')
    ts = []
    cs = []
    ps = []
    for l in f.readlines():
        values = l.strip("\n").split(delimiter)
        ts.append(float(values[0]))
        cs.append(values[1])
        if len(values) >= 3: # there might not be a port defined
            p = values[2]
            if p != "": 
                ps.append(p.strip(" "))
    return ts, cs, ps

reps = 2
baudrate = 38400
fname = 'test.csv'
ts, cs, ps = load_csv(fname)

if len(ps) == 1:
    ps = ps*len(ts)
    

ports = list(set(ps))
serials = {} # serial connections
for port in ports:
    ser = serial.Serial(port = port, 
                        baudrate=baudrate,
                        write_timeout=0,
                        bytesize=serial.EIGHTBITS,
                        stopbits=serial.STOPBITS_ONE,
                        parity=serial.PARITY_NONE)
    serials[port] = ser
    


cs_rep = cs*reps
ts_rep = []
for r in range(reps):
    for t in ts:
        ts_rep.append(t + ts[-1]*r)

ps_reps = ps*reps

runcommands(cs_rep, ts_rep, ps_reps, serials, verbose=True)
    
time.sleep(0.5)
for ser in serials.values():
    ser.close()