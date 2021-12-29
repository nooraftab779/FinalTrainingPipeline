from django.core.management.base import BaseCommand, CommandError
import socket
from server.models import ServerManagement, CpuUsage
import ast
import threading
from queue import Queue
import time

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]  # 1 is to listen connection & accept connection, 2 is to send command with existing client
queue = Queue()
all_connections = []
all_address = []


def create_socket():
    try:
        global s
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


def bind_socket():
    try:
        global host
        global port
        global s
        # hostname = socket.gethostname()
        # IPAddr = socket.gethostbyname(hostname)
        host = '192.168.88.140'
        port = 5001
        print("Connection established: " + str(host) + ':' + str(port))
        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


def accepting_connections():
    while True:
        try:
            c, address = s.accept()
            all_address.append(address)
            all_connections.append(c)
            print("Established connections:", address[0])
        except:
            print("error in establishing connection with client.")


def server_status_update():
    while 1:
        for i, conn in enumerate(all_connections):
            try:
                data = conn.recv(1024)
                ls = ast.literal_eval(data.decode("utf-8"))
                server_name = ls[0]
                if not ServerManagement.objects.filter(server_name=server_name, ip_addr=all_address[i][0]).exists():
                    processor = ls[1]
                    ram = ls[2]
                    print()
                    ServerManagement.objects.create(server_name=server_name, ip_addr=all_address[i][0], ram=ram,
                                                    processor=processor, enable=True)
                elif ServerManagement.objects.filter(server_name=server_name, ip_addr=all_address[i][0],
                                                     enable=False).exists():
                    ServerManagement.objects.filter(server_name=server_name, ip_addr=all_address[i][0]).update(
                        enable=True)
                elif ServerManagement.objects.filter(server_name=server_name, ip_addr=all_address[i][0],
                                                     enable=True).exists():
                    result = ServerManagement.objects.get(server_name=server_name, ip_addr=all_address[i][0])
                    CpuUsage.objects.create(server_id=result, cpu=ls[3], ram=0)

            except:
                result = ServerManagement.objects.filter(ip_addr__iexact=all_address[i][0]).update(enable=False)
                CpuUsage.objects.filter(server_id=result).delete()
                print("Connection is lost! Ip: ", all_address[i][0])
                del all_connections[i]
                del all_address[i]


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            server_status_update()
        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_workers()
        create_jobs()
