# -*- coding: utf-8 -*-

import serial
import time
import argparse

     
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


def load_csv(f):
    delimiter = ','
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

# Create argument parser
    
parser = argparse.ArgumentParser(description='sends a series of commands over the serial port')
parser.add_argument('filename',
                    type=str, help='CSV file with columns for time, commands and ports')
parser.add_argument('-r', '--reps', required = False, default=1,
                    type=int, help='Number of command sequence repetitions (default: %(default)s)')
parser.add_argument('-bd', '--baudrate', required = False, default=38400,
                    type=int, help='Baudrate (default: %(default)s)')
parser.add_argument('-v', '--verbose', required = False,
                    action='store_true',
                    help='Print Commands as they are sent (default: %(default)s)')
parser.add_argument('-p', '--profiling', required = False,
                    action='store_true',
                    help='Show profiling information if verbose (default: %(default)s).')
    
# Get parameters
args = parser.parse_args()
#print(args.filename)
#print(args.reps)
#print(args.baudrate)
#print(args.verbose)
#print(args.profiling)

# Parameters
fname = args.filename
reps = args.reps
baudrate = args.baudrate
verbose = args.verbose
profiling = args.profiling

# test.csv -r 2 -b 38400 -v -p
#fname = 'test.csv'
#reps = 2
#baudrate = 38400
#verbose = True
#profiling = True
try: 
    f = open(fname, 'r')
    ts, cs, ps = load_csv(f)

    # Repeat all lists the specified number of times
    ts_rep = [] # offset each rep's times
    for r in range(reps):
        for t in ts:
            ts_rep.append(t + ts[-1]*r)
    cs_rep = cs*reps
    ps_reps = ps*reps
    
    # Try to open the serial port connections and run the commands

    try:
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
        runcommands(cs_rep, ts_rep, ps_reps, serials, verbose, profiling)
    finally:
        time.sleep(0.5)
        for ser in serials.values():
            ser.close()
finally:
    f.close()