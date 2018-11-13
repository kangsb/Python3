# -*- coding: utf8 -*-
#!/usr/bin/env python
"""
An annotated simple socket server example in python.

WARNING: This example doesn't show a very important aspect of
TCP - TCP doesn't preserve message boundaries. Please refer
to http://blog.stephencleary.com/2009/04/message-framing.html
before adapting this code to your application.

Runs in both python2 and python3.
"""
import socket

# Optionally set a specific address. This (the empty string) will listen on all
# the local machine's IPv4 addresses. It's a common way to code a general
# purpose server. If you specify an address here, the client will need to use
# the same address to connect.
SERVER_ADDRESS = ''

# Can change this to any port 1-65535 (on many machines, ports <= 1024 are
# restricted to privileged users)
SERVER_PORT = 22222

# Create the socket
s = socket.socket()

# Optional: this allows the program to be immediately restarted after exit.
# Otherwise, you may need to wait 2-4 minutes (depending on OS) to bind to the
# listening port again.
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to the desired address(es) and port. Note the argument is a tuple: hence
# the extra set of parentheses.
s.bind((SERVER_ADDRESS, SERVER_PORT))

# How many "pending connections" may be queued. Exact interpretation of this
# value is complicated and operating system dependent. This value is usually
# fine for an experimental server.
s.listen(5)

print("Listening on address %s. Kill server with Ctrl-C" %
      str((SERVER_ADDRESS, SERVER_PORT)))

# Now we have a listening endpoint from which we can accept incoming
# connections. This loop will accept one connection at a time, then service
# that connection until the client disconnects. Lather, rinse, repeat.
while True:
    c, addr = s.accept()
    print("\nConnection received from %s" % str(addr))

    while True:
        data = c.recv(2048)
        if not data:
            print("End of file from client. Resetting")
            break

        # Decode the received bytes into a unicode string using the default
        # codec. (This isn't strictly necessary for python2, but, since we will
        # be encoding the data again before sending, it works fine there too.)
        data = data.decode()

        print("Received '%s' from client" % data)

        data = "Hello, " + str(addr) + ". I got this from you: '" + data + "'"

        # See above
        data = data.encode()

        # Send the modified data back to the client.
        c.send(data)

    c.close()