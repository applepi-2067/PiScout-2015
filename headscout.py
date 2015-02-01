from queue import Queue
from threading import Thread
import tkinter as tk
import bluetooth

queue = Queue()

def bluetooth_server():
    print('started new thread for server')
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    server_socket.bind(("", 27))
    print('server started')

    server_socket.listen(2)
    print('listening for clients')

    while True:
        client_socket, client_info = server_socket.accept();
        name = bluetooth.lookup_name(client_info[0], 4)
        print('accepted connection from', name);
        Thread(target = client_handler, args = [client_socket, name]).start()

    data = client_socket.recv(1024);
    print("received:", data)

    server_socket.close()
    client_socket.close()

def client_handler(client_socket, name):
    print('started new thread for client', name)
    while True:
        data = client_socket.recv(1024)
        if len(data) > 1:
            print('%s: %s' % (name, data))
            
            if data == 'close':
                client_socket.close()
                print('disconnected from', name)
                break
            
            queue.put(data)
            print('data added to queue')


def update_data(data):
    print('processing data: ', data)

app = tk.Tk()
app.title('Head Scout')
app.geometry('450x300+200+200')

label = tk.Label(app, text='Head Scout', height=4)
label.pack()
button = tk.Button(app, text='Start Server', width=20,
                 command=Thread(target=bluetooth_server).start)
button.pack()

app.mainloop();

#while True:
#    if not queue.empty():
#        print 'reading data from queue'
#        update_data(queue.get())
