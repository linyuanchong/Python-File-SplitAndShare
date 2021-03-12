
import socket
import hashlib
from datetime import datetime

HOST = 'localhost'

PORT = 50007

#Used for storing the list of available songs.
register = list()

#Manually adding a song to test romoval.
register.append("britney.mp3-localhost:5007")

print("Client or server")

inp = input()

if "c" in inp:

    print("Starting client")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        while True:
            print("Please enter a command:")
            inp = input()
            #Overwriting waiting process.
            #s.sendall(bytes(inp, 'utf8'))
            #data = s.recv(1024)
            #print('Received', repr(data))

            #Send file command.
            if '<ping' in inp:
                s.sendall(bytes(inp, 'utf8'))
                data = s.recv(1024)
                print('Received', repr(data))

            #Show local ip command of user.
            elif '<showip' in inp:
                hostname = socket. gethostname()
                local_ip = socket. gethostbyname(hostname)
                print("Your local ip address: " + (local_ip))

            elif "<sendfile" in inp:
                print ("Sending the file...")

                #Spilt command into two parts.
                parts = inp.split('-')
                command = parts[0]
                filename = parts[1]

                #Send a command to tell the server to save the files.
                s.sendall(bytes('<savefile', 'utf-8'))

                #Open a stream(rb = read bytes).
                with open(filename, 'rb') as reader:
                    print("Reading in from file...")
                    data = reader.readline()
                    #Send the bytes.
                    s.sendall(data)
            
            elif "<hash>" in inp:
                print("hashing")
                hashinput = input()
                hash = hashlib.sha224(hashinput.encode()).hexdigest()
                s.sendall(bytes(hashinput + '-' + hash, 'utf8'))

            else: 
                s.sendall(bytes(inp, 'utf8'))
                #data = s.recv(1024)
                #print('Received', repr(data))



else:
    print("Starting server")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print ('Connected by', addr)
            while True:
                data = conn.recv(1024)
            
                data = str(data)
            
                if "<help>" in data:
                    #Help command.
                    print("Running help")
                    conn.sendall(bytes("Running help", 'utf8'))
            
                elif "<time>" in data:
                    #Check time command.
                    print("Running time code")
                    conn.sendall(bytes("Running time", 'utf8'))
            
                elif "<ping>" in data:
                    #Ping command.
                    print("Got a ping")
                    serverTime = ''
                    output = ''
                    #Get time from local machine.
                    serverTime = str(datetime.now())
                    output = '<pong-' + serverTime + '>'
                    conn.sendall(bytes(output, 'utf8'))

                #Add song command.
                #<addsong-britney.mp3-localhost
                elif "<addsong" in data:
                    print("Found song command")
                    #Split command with '-'.
                    parts = data.split('-')
                    #1: Add command.
                    print("Part 1: " + parts[0])
                    #2: File name.
                    print("Part 2: " + parts[1])
                    #3: Who has the song.
                    print("Part 3: " + parts[2])
                    register.append(parts[1] + parts[2])

                #Remove song command.
                #<removesong-britney.mp3-localhost>
                elif "<removesong" in data:
                    parts = data.split('-')
                    print("Part 1 " + parts[0])
                    print("Part 2 " + parts[1])
                    print("Part 3 " + parts[2])

                    for song in register:
                        print(song)
                        if parts[1] in song:
                            register.remove(song)

                #Save file command.
                #<savefile-britney.mp3
                elif "<savefile" in data:
                    print("Rec file")
                    data = conn.recv(600000000)

                    f = open('output.mp3', 'wb')
                    f.write(data)
                    f.close()
                    print("File created")

                #Find song command.
                #<find-britney.mp3
                elif "<find" in data: 
                    print("finding song")
                    parts = data.split('-')
                    print("Part 1 " + parts[0])
                    print("Part 2 " + parts[1])
                    for x in register:
                        if parts[1][:-1] in x:
                            print(x)
                
                #Show local ip command.
                elif "<showip" in data:
                    hostname = socket. gethostname()
                    local_ip = socket. gethostbyname(hostname)
                    print(local_ip)


