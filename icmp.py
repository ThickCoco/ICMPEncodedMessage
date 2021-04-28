#!/usr/bin/env python


import os, sys, socket, struct, select, time


ICMP_ECHO_REQUEST = 8 # Seems to be the same on Solaris.


def checksum(source_string):
    sum = 0
    countTo = (len(source_string)/2)*2
    count = 0

    while count<countTo:
        thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
        sum = sum + thisVal
        sum = sum & 0xffffffff
        count = count + 2

    if countTo<len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff

    sum = (sum >> 16)  +  (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


def receive_one_ping(my_socket, ID, timeout):
    timeLeft = timeout

    while True:
        startedSelect = time.clock()
        whatReady = select.select([my_socket], [], [], timeLeft)
        howLongInSelect = (time.clock() - startedSelect)

        if whatReady[0] == []:
            return

        timeReceived = time.clock()
        recPacket, addr = my_socket.recvfrom(1024)
        icmpHeader = recPacket[20:28]
        type, code, checksum, packetID, sequence = struct.unpack(
            "bbHHh", icmpHeader
        )

        if packetID == ID:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - timeSent

        timeLeft = timeLeft - howLongInSelect

        if timeLeft <= 0:
            return


def send_one_ping(my_socket, dest_addr, ID, msg):
    dest_addr  =  socket.gethostbyname(dest_addr)

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    my_checksum = 0

    # Make a dummy heder with a 0 checksum.
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    bytesInDouble = struct.calcsize("d")
    data = msg
    data = struct.pack("d", time.clock()) + data

    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(header + data)

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack(
        "bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1
    )

    packet = header + data

    my_socket.sendto(packet, (dest_addr, 1)) # Don't know about the 1


def do_one(dest_addr, timeout, msg):
    icmp = socket.getprotobyname("icmp")

    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

    except socket.error, (errno, msg):
        if errno == 1:
            msg = msg + (
                " - Note that ICMP messages can only be sent from processes"
                " running as root."
            )
            raise socket.error(msg)

        raise # raise the original error

    my_ID = os.getpid() & 0xFFFF

    send_one_ping(my_socket, dest_addr, my_ID, msg)

    delay = receive_one_ping(my_socket, my_ID, timeout)

    my_socket.close()

    return delay


def verbose_ping(dest_addr, msg, timeout = 2):
    print "ping %s..." % dest_addr,
    try:
        delay  =  do_one(dest_addr, timeout, msg)

    except socket.gaierror, e:
        print "failed. (socket error: '%s')" % e[1]
        return

    if delay  ==  None:
        print "failed. (timeout within %ssec.)" % timeout

    else:
        delay  =  delay * 1000

    print "get ping in %0.4fms" % delay


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Numero de argumentos erroneos."
        print "arg1: IP dest; arg2: Fichero a mandar"
        sys.exit()

    ip = sys.argv[1]
    name = sys.argv[2]

    file = open(name, 'r')
    size = os.stat(name).st_size

    print size

    while size > 0:
        msg = file.read(500)
        verbose_ping(ip, msg)
        size = size - 500





