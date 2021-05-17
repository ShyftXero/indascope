#!/usr/bin/env python3
import ipaddress
import socket
import string
import sys
import re
from pathlib import Path
from typing import List, Optional, Union


import typer
from rich import print

INSTALL_DIR = Path(__file__).parent
VERBOSE = False

app = typer.Typer()


# @app.command()
def get_ip(host:str, verbose=True, loading_scope=False) -> ipaddress.IPv4Address:
    """resolves a hostname to an ip; not much different than pinging it to get the ip except no traffic"""
    ip_addr = None
    try:
        ip_addr = ipaddress.IPv4Address(socket.gethostbyname(host))
    except socket.gaierror as e:
        if loading_scope == True: 
            print(host, e, '; bad domain or hostname in scope file? ')
    except ValueError as e:
        print(e)
        exit()

    return ip_addr



def build_targets(scope_file) -> set:
    targets = set()
    try:
        f = open(scope_file)
        f.close()
    except FileNotFoundError as e:
        try:
            f = open('~/in_scope.txt')
            f.close()
            scope_file = '~/in_scope.txt'
        except FileNotFoundError as e2:
            if VERBOSE:
                print('failed to load from ~/in_scope.txt')

            print(e)
            print(e2)
            sys.exit()

    with open(scope_file) as f:
        lines = f.readlines()
        for line in lines:
            
            line = line.split('#') # allow for # based comments 
            line = line[0].strip()
            # print('line =', line)
            if line == '': # skip blank lines
                continue
            elif re.search(r'([0-9]{1,3}\.?){4}$', line): # for basic ip address
                if VERBOSE:
                    print('is an ip ', line)
                targets.add(ipaddress.IPv4Address(line))   
            elif re.search(r'\d\/\d*$', line): # for cidr networks e.g. 10.0.0.0/8
                if VERBOSE:
                    print('is a cidr', line)
                ip_net = ipaddress.ip_network(line)
                net = [ip for ip in ip_net] # add all the ips to the set... 
                targets.update(net)
            elif re.search(r'\w', line): # is a hostname... we need the ip 
                if VERBOSE:
                    print('is a hostname', line)
                ip = get_ip(line, loading_scope=True)       
                targets.add(ip)         # add the ip to the set
                targets.add(line)       # and the hostname...    
    try:
        targets.remove(None) # remove erroneous entries to the set      
    except KeyError as e:
        pass

    if VERBOSE:
        num_targets = len(targets)
        if num_targets < 512:
            print(targets)  # rich.print is slow on large collections. 
        print(f'Total in scope IPS: {num_targets}')
        print('-'*30)

    return targets

def check(potential_targets, in_scope_targets, verbose=False):
    if type(potential_targets) == str:
        potential_targets=[potential_targets,'']

    for addr in potential_targets:
        addr = addr.strip()
        
        try:
            ip = ipaddress.IPv4Address(addr)
        except ipaddress.AddressValueError as e:
            # print(addr, e)
            ip = get_ip(addr)

        if ip in in_scope_targets:
            try:
                if addr != ip.compressed:
                    print(f'{addr} -> {ip}')
                else:
                    print(ip.compressed)
            except AttributeError as e:
                print(ip.compressed) 
            except BaseException as e:
                print(e)


@app.command()
def in_scope(targets:List[str]=typer.Argument(None), target_file:Path=None, scope_file:Path=f'./in_scope.txt', verbose:bool=typer.Option(False, '-v')):
    """Checks to see if one or more host IPs are in the scope file; """
    if verbose == True:
        global VERBOSE
        VERBOSE = True

    in_scope_ips = build_targets(scope_file)
        
    if len(targets) == 0  and target_file == None:
        # print('using stdin')
        targets = sys.stdin.read().splitlines(keepends=False)
    elif target_file != None:
        with open(target_file) as f:
            targets = f.read().splitlines(keepends=False)

    check(targets, in_scope_ips)
    

if __name__ == '__main__':
    
    app()
