#!/usr/bin/env python3
import ipaddress
import socket
import string
import sys
import re
from pathlib import Path
from typing import List, Optional, Union
from mpire import WorkerPool


import typer
og_print = print
from rich import print

__VERSION__ = '' # this is updated with make release which rebuilds 

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



def build_scope(scope_file, showing:bool=False) -> set:
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
                
                ip_net = ipaddress.ip_network(line, strict=False)
                
                net = [ip for ip in ip_net] # add all the ips to the set... 
                if VERBOSE:
                    print(f'is a cidr {line} with {len(net)} IPs starting at {net[0]} and ending at {net[-1]}')
                targets.update(net)
            elif re.search(r'\w', line): # is a hostname... we need the ip 
                
                ip = get_ip(line, loading_scope=True)   
                if VERBOSE:
                    print(f'is a hostname "{line}" with ip {ip}')    
                targets.add(ip)         # add the ip to the set
                targets.add(line)       # and the hostname...    
    try:
        targets.remove(None) # remove erroneous entries to the set      
    except KeyError as e:
        pass

    # if VERBOSE and showing == False:
    #     num_targets = len(targets)
    #     if num_targets < 512:
    #         print(targets)  # rich.print is slow on large collections. 
    #     print(f'Total in scope IPS: {num_targets}')
    #     print('-'*30)
    
    return targets

def check(in_scope_targets, potential_targets, verbose=False):
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
def in_scope(targets:List[str]=typer.Argument(None), target_file:Path=None, scope_file:Path=f'./in_scope.txt', verbose:bool=typer.Option(False, '-v'), show:bool=typer.Option(False, '--show-ips', '-s'), version:bool=typer.Option(False, '--version')):
    """Checks to see if one or more host IPs are in the scope file; """
    if version:
        print(__VERSION__)
        sys.exit()
    if verbose == True:
        global VERBOSE
        VERBOSE = True

    in_scope_targets = build_scope(scope_file, showing=show)

    if show:
        in_scope_host : ipaddress.IPv4Address
        # for in_scope_host in in_scope_targets: # 10 seconds for example scope; 65k ips
        #     if type(in_scope_host) == ipaddress.IPv4Address:

        #     print(str(in_scope_host))

        ips=[str(x) for x in in_scope_targets]
        print(sorted(ips)) # 5 seconds ; 65k ips
        if VERBOSE:
            print(f'Total in scope hosts (IPs and hostnames): {len(in_scope_targets)}')
        sys.exit()


    
    if len(targets) == 0  and target_file == None:
        # print('using stdin')
        targets = sys.stdin.read().splitlines(keepends=False)
    elif target_file != None:
        with open(target_file) as f:
            targets = f.read().splitlines(keepends=False)


    with WorkerPool(shared_objects=in_scope_targets) as pool:
        # https://slimmer-ai.github.io/mpire/v2.1.0/usage/worker_pool.html#shared-objects
        # pool.set_shared_objects(in_scope_ips) # another way to do this inside of 
        pool.map(check, targets)

    # check(targets, in_scope_ips)
    

if __name__ == '__main__':
    
    app()
