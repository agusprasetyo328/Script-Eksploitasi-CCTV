def check_port(port):
      return port >= 40000
def separate_ports(dns_list):
    real_ports = []
    port_scanner_ports = []
    for dns in dns_list:
        # Misalkan Anda mendapatkan port dari DNS
        # Di sini saya menggunakan nilai acak sebagai contoh
        port = int(dns[-4:])
        if check_port(port):
            port_scanner_ports.append(port)
        else:
            real_ports.append(port)
    return real_ports, port_scanner_ports
# Contoh pemanggilan fungsi dengan daftar DNS
dns_list = ["example.com:12345", "example.net:50000", "example.org:55555"]
real_ports, port_scanner_ports = separate_ports(dns_list)
print("Port Asli:", real_ports)
print("Port Scanner:", port_scanner_ports)