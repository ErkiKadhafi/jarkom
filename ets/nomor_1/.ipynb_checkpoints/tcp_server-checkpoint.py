import sys
import socket
import logging
import json
import dicttoxml
import os
import ssl

alldata = dict()
alldata['1']=dict(nomor=1, nama="dean henderson", posisi="kiper")
alldata['2']=dict(nomor=2, nama="luke shaw", posisi="bek kiri")
alldata['3']=dict(nomor=3, nama="aaron wan-bissaka", posisi="bek kanan")
alldata['4']=dict(nomor=4, nama="victor lindelof", posisi="bek tengah kanan")
alldata['5']=dict(nomor=5, nama="victor lindelof 5", posisi="bek tengah kanan 5")
alldata['6']=dict(nomor=6, nama="victor lindelof 6", posisi="bek tengah kanan 6")
alldata['7']=dict(nomor=7, nama="victor lindelof 7", posisi="bek tengah kanan 7")
alldata['8']=dict(nomor=8, nama="victor lindelof 8", posisi="bek tengah kanan 8")
alldata['9']=dict(nomor=9, nama="victor lindelof 9", posisi="bek tengah kanan 9")
alldata['10']=dict(nomor=10, nama="victor lindelof 10", posisi="bek tengah kanan 10")
alldata['11']=dict(nomor=11, nama="victor lindelof 11", posisi="bek tengah kanan 11")
alldata['12']=dict(nomor=12, nama="victor lindelof 12", posisi="bek tengah kanan 12")
alldata['13']=dict(nomor=13, nama="victor lindelof 13", posisi="bek tengah kanan 13")
alldata['14']=dict(nomor=14, nama="victor lindelof 14", posisi="bek tengah kanan 14")
alldata['15']=dict(nomor=15, nama="victor lindelof 15", posisi="bek tengah kanan 15")
alldata['16']=dict(nomor=16, nama="victor lindelof 16", posisi="bek tengah kanan 16")
alldata['17']=dict(nomor=17, nama="victor lindelof 17", posisi="bek tengah kanan 17")
alldata['18']=dict(nomor=18, nama="victor lindelof 18", posisi="bek tengah kanan 18")
alldata['19']=dict(nomor=19, nama="victor lindelof 19", posisi="bek tengah kanan 19")
alldata['20']=dict(nomor=20, nama="victor lindelof 20", posisi="bek tengah kanan 20")

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

def run_server(server_address,is_secure=False):
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

        try:
            connection = koneksi

            selesai=False
            data_received="" #string
            while True:
                data = connection.recv(32)
                logging.warning(f"received {data}")
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
                        break

                else:
                   logging.warning(f"no more data from {client_address}")
                   break
            # Clean up the connection
        except ssl.SSLError as error_ssl:
            logging.warning(f"SSL error: {str(error_ssl)}")

if __name__=='__main__':
    try:
        run_server(('0.0.0.0', 12000),is_secure=False)
    except KeyboardInterrupt:
        logging.warning("Control-C: Program berhenti")
        exit(0)
    finally:
        logging.warning("seelsai")
