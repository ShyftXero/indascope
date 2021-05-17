# indascope
Check to see if one or more hosts is in... the... scope... 

useful for validating the output of some other tool like subfinder from projectdiscovery.io

searches the current directory for `in_scope.txt`. if that fails it searches your home directory (`~/in_scope.txt) 


```
Usage: indascope [OPTIONS] [TARGETS]...

  Checks to see if one or more host IPs are in the scope file;

Arguments:
  [TARGETS]...

Options:
  --target-file PATH
  --scope-file PATH               [default: ./in_scope.txt]
  -v                              [default: False]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help   
```
OR

```bash
cat possible_targets.txt | indascope 
```

OR

```bash
indascope 12.34.13.37 vuln.target.com 1.2.3.4
```

OR

```bash
indascope -f list_of_potenttial_targets.txt
```
## Scope files (in_scope.txt)
scope files are just lines of IP addresses, CIDR ranges, and/or domain/hostnames

one per line
```
12.34.13.37
1.1.1.1
some.domain.com
another.domain.com
172.16.0.0/16
```



## Install from source
run `make develop` then `make build` then run `make install` and it will copy to `/usr/bin/indascope`
