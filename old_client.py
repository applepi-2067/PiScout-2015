import bluetooth

server_address = None

print('searching for server')
nearby_devices = bluetooth.discover_devices()

for address in nearby_devices:
    if bluetooth.lookup_name(address, 8) == 'APPLEPI-PC':
        server_address = address
        break

if server_address is not None:
    print('found server with address', server_address)
else:
    print('could not find server')
    exit()

socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
socket.connect((server_address, 27))
print('successfully connected to server')

def send(msg):
    socket.send(msg)
    print('sent: ', msg)

send('test 1')
send('test 2')
send('close')

socket.close()
