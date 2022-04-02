import socket
import json
import logging

import concurrent.futures
import random
import datetime

server_address = ('172.16.16.101', 12000)

def make_socket(destination_address='localhost',port=12000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        return sock
    except Exception as ee:
        logging.warning(f"error {str(ee)}")

def deserialisasi(s):
    logging.warning(f"deserialisasi {s.strip()}")
    return json.loads(s)
    # return s

def send_command(command_str,is_secure=False):
    alamat_server = server_address[0]
    port_server = server_address[1]
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # gunakan fungsi diatas
    sock = make_socket(alamat_server,port_server)

    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = deserialisasi(data_received)
        logging.warning("data received from server:")
        return hasil
    except Exception as ee:
        logging.warning(f"error during data receiving {str(ee)}")
        return False

def getdatapemain(nomor=0,is_secure=False):
    cmd=f"getdatapemain {nomor}\r\n\r\n"
    hasil = send_command(cmd,is_secure=is_secure)
    return hasil

def lihatversi(is_secure=False):
    cmd=f"versi \r\n\r\n"
    hasil = send_command(cmd,is_secure=is_secure)
    return hasil
    
def req_data_with_thread(threadNumber, requestNumber=20):
    texec = dict()
    status_task = dict()
    task = concurrent.futures.ThreadPoolExecutor(max_workers=threadNumber)
    time_start = datetime.datetime.now()
    
    # request number 
    for i in range(1,requestNumber+1):
        index = random.randint(1,20)
        texec[i] = task.submit(getdatapemain, index)
    time_process = datetime.datetime.now() - time_start
    
    counter = 0
    for i in range(1,requestNumber+1):
        if(texec[i].result() != None): 
            counter += 1
        status_task[f"result-{i}"] = texec[i].result()

    return [status_task, time_process, counter]

def print_dictionary_with_format(data):
    for key in data:
        print(f"{key} :\t {data[key]}")    

if __name__=='__main__':
    texec = dict()
    [status_task1, time_process1, counter1] = req_data_with_thread(1, 20)
    [status_task2, time_process2, counter2] = req_data_with_thread(5, 20)
    [status_task3, time_process3, counter3] = req_data_with_thread(10, 20)
    [status_task4, time_process4, counter4] = req_data_with_thread(20, 20)

    print("\n")
    print(f"RESULT WITH 1 THREAD, 20 REQUESTS with time {time_process1} seconds. Number of results {counter1}")
    # print_dictionary_with_format(status_task1)
    print("\n") 

    print(f"RESULT WITH 5 THREAD, 20 REQUESTS with time {time_process2} seconds. Number of results {counter2}")
    # print_dictionary_with_format(status_task2)
    print("\n")

    print(f"RESULT WITH 10 THREAD, 20 REQUESTS with time {time_process3} seconds. Number of results {counter3}")
    # print_dictionary_with_format(status_task3)
    print("\n")

    print(f"RESULT WITH 20 THREAD, 20 REQUESTS with time {time_process4} seconds. Number of results {counter4}")
    # print_dictionary_with_format(status_task4)
    