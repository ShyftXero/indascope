# indascope
Check to see if one or more hosts is in... the... scope... 

useful for validating the output of some other tool subfinder

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
