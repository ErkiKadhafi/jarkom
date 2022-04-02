import socket
import logging
import json
import ssl
import os
from time import sleep

from make_json import make_json_data
import time
import threading

alldata = make_json_data()
thread_list = []

def versi():
    return "versi 0.0.1"

def proses_request(request_string):
    #format request
    # NAMACOMMAND spasi PARAMETER
    cstring = request_string.split(" ")
    hasil = None
    try:
        command = cstring[0].strip()
        if (command == 'getdatapemain'):
            # getdata spasi parameter1
            # parameter1 harus berupa nomor pemain
            logging.warning("getdata")
            nomorpemain = cstring[1].strip()
            try:
                logging.warning(f"data {nomorpemain} ketemu")
                hasil = alldata[nomorpemain]
            except:
                hasil = None
        elif (command == 'versi'):
            hasil = versi()
    except:
        hasil = None
    return hasil


def serialisasi(a):
    serialized =  json.dumps(a)
    logging.warning("serialized data")
    logging.warning(serialized)
    return serialized

def handle_client(koneksi, client_address, socket_context):
    try:
        connection = socket_context.wrap_socket(koneksi, server_side=True)
        selesai=False
        data_received="" #string
        threadName = threading.current_thread().native_id
        while True:
            data = connection.recv(32)
            # time.sleep(1)
            logging.warning(f"[Thread - {threadName}] received {data}")
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    selesai=True

                if (selesai==True):
                    hasil = proses_request(data_received)
                    logging.warning(f"hasil proses: {hasil}")

                    hasil = serialisasi(hasil)
                    hasil += "\r\n\r\n"
                    connection.sendall(hasil.encode())
                    selesai = False
                    data_received = ""  # string
                    
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    print(f"[Thread - {threadName}] BERHASIL MENGHANDLE CLIENT")
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    break 
            else:
                logging.warning(f"no more data from {client_address}")
                connection.close()
                return None
                break
        # Clean up the connection
    except ssl.SSLError as error_ssl:
        logging.warning(f"SSL error: {str(error_ssl)}")


def run_server(server_address,is_secure=False):
    # ------------------------------ SECURE SOCKET INITIALIZATION ----
    if is_secure == True:
        print(os.getcwd())
        cert_location = os.getcwd() + '/certs/'
        socket_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        socket_context.load_cert_chain(
            certfile=cert_location + 'domain.crt',
            keyfile=cert_location + 'domain.key'
        )
    # ---------------------------------

    #--- INISIALISATION ---
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    logging.warning(f"starting up on {server_address}")
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1000)

    while True:
        # Wait for a connection
        logging.warning("waiting for a connection")
        koneksi, client_address = sock.accept()
        logging.warning(f"Incoming connection from {client_address}")
        # Receive the data in small chunks and retransmit it

        threadExe = threading.Thread(target=handle_client, args=(koneksi, client_address, socket_context))
        threadExe.start()

if __name__=='__main__':
    try:
        run_server(('0.0.0.0', 12000),is_secure=True)
    except KeyboardInterrupt:
        logging.warning("Control-C: Program berhenti")
        exit(0)
    finally:
        # for thread in thread_list:
        #     thread.join()
        logging.warning("seelsai")
