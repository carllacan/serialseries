# -*- coding: utf-8 -*-

import serial
import time

     
def write_command(serial, comm, verbose = False, dt = None):
    """ Encodes a command and sends it over the serial port """
    if verbose and comm != "":
        if dt is None:
           print("{} \t\t-> {}".format(comm, serial.port))
        else:
            print("{} \t\t-> {} at {:2.3f} ms".format(comm, serial.port, dt))
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
        

def runcommands(cs, ts, ps, serials, verbose = False, profiling = False):
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
            if profiling:
                write_command(ser, comm, verbose, dt)
            else:
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
        if len(values) <= 3: # if there isn't a third field
            values.append("") # add an empty one
        p = values[2].strip(" ") # take all spaces out
        if p == "": 
            ps.append(ps[-1]) # use previous one if it's empty
        else:
            ps.append(p)
    return ts, cs, ps

fname = 'test.csv'
reps = 2
baudrate = 38400
verbose = True
profiling = True

ts, cs, ps = load_csv(fname)

# Get list of unique portnames
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
    

# Repeat all lists the specified number of times
ts_rep = [] # offset each rep's times
for r in range(reps):
    for t in ts:
        ts_rep.append(t + ts[-1]*r)
cs_rep = cs*reps
ps_reps = ps*reps

runcommands(cs_rep, ts_rep, ps_reps, serials, verbose, profiling)
    
time.sleep(0.5)
for ser in serials.values():
    ser.close()