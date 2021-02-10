from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


def cek_input_ip(input_ip):
    # Validasi IP
    octet_ip = input_ip.split(".")
    try:
        int_octet_ip = [int(i) for i in octet_ip]

        if (len(int_octet_ip) == 4) and \
                (int_octet_ip[0] != 127) and \
                (int_octet_ip[0] != 169) and \
                (0 <= int_octet_ip[1] <= 255) and \
                (0 <= int_octet_ip[2] <= 255) and \
                (0 <= int_octet_ip[3] <= 255):
            return int_octet_ip
        else:
            return 0
    except ValueError:
        return 0


def cek_input_netmask(input_netmask):
    # Subnet mask
    masks = [0, 128, 192, 224, 240, 248, 252, 254, 255]

    # Validasi Netmask
    octet_netmask = input_netmask.split(".")
    try:
        int_octet_netmask = [int(i) for i in octet_netmask]
        if (len(int_octet_netmask) == 4) and \
                (int_octet_netmask[0] == 255) and \
                (int_octet_netmask[1] in masks) and \
                (int_octet_netmask[2] in masks) and \
                (int_octet_netmask[3] in masks) and \
                (int_octet_netmask[0] >= int_octet_netmask[1] >= int_octet_netmask[2] >= int_octet_netmask[3]):
            return int_octet_netmask
        else:
            return 0
    except ValueError:
        return 0


# Ubah IP dan Netmask menjadi biner
def hitung_subnetting(input_ip, input_netmask, int_octet_ip, octet_subnet):
    try:
        ip_in_binary = []

        # Ubah setiap oktet IP menjadi biner
        ip_in_binary_octets = [bin(i).split("b")[1] for i in int_octet_ip]

        # Ubah setiap oktet biner sepanjang 8 bit dengan memasukkan angka 0
        for i in range(0, len(ip_in_binary_octets)):
            if len(ip_in_binary_octets[i]) < 8:
                padded_binary = ip_in_binary_octets[i].zfill(8)
                ip_in_binary.append(padded_binary)
            else:
                ip_in_binary.append(ip_in_binary_octets[i])

        ip_binary_mask = "".join(ip_in_binary)

        netmask_in_binary = []

        # Konversi setiap octet netmask ke biner
        netmask_binary_octet = [bin(i).split("b")[1] for i in octet_subnet]

        # Buat setiap oktet biner sepanjang 8 bit dengan memasukkan angka 0
        for i in netmask_binary_octet:
            if len(i) < 8:
                netmask_padded = i.zfill(8)
                netmask_in_binary.append(netmask_padded)
            else:
                netmask_in_binary.append(i)

        # Cetak
        netmask_binary_mask = "".join(netmask_in_binary)

        # Menghitung jumlah host
        no_zeros = netmask_binary_mask.count("0")
        no_ones = 32 - no_zeros
        no_hosts = abs(2 ** no_zeros - 2)

        # Menghitung wildcard mask
        wild_mask = []
        for i in octet_subnet:
            wild_bit = 255 - i
            wild_mask.append(wild_bit)

        wildcard = ".".join([str(i) for i in wild_mask])

        # Menghitung network dan broadcast alamat
        network_add_binary = ip_binary_mask[:no_ones] + "0" * no_zeros
        broadcast_add_binary = ip_binary_mask[:no_ones] + "1" * no_zeros

        network_add_binary_octet = []
        broadcast_binary_octet = []

        [network_add_binary_octet.append(i) for i in [network_add_binary[j:j + 8]
                                                      for j in range(0, len(network_add_binary), 8)]]
        [broadcast_binary_octet.append(i) for i in [broadcast_add_binary[j:j + 8]
                                                    for j in range(0, len(broadcast_add_binary), 8)]]

        network_add_final = ".".join([str(int(i, 2)) for i in network_add_binary_octet])
        broadcast_add_final = ".".join([str(int(i, 2)) for i in broadcast_binary_octet])

        # Menghitung rentang IP host
        first_ip_host = network_add_binary_octet[0:3] + [(bin(int(network_add_binary_octet[3], 2) + 1).split("b")[1].zfill(8))]
        first_ip = ".".join([str(int(i, 2)) for i in first_ip_host])

        last_ip_host = broadcast_binary_octet[0:3] + [(bin(int(broadcast_binary_octet[3], 2) - 1).split("b")[1].zfill(8))]
        last_ip = ".".join([str(int(i, 2)) for i in last_ip_host])

        # Cetak semua perhitungan
        txt_hasil.insertPlainText(f"Network\t   : {network_add_final}" + "\n")
        txt_hasil.insertPlainText(f"Subnet Mask\t   : {'.'.join(map(str, octet_subnet))}" + "\n")
        txt_hasil.insertPlainText(f"Host Pertama   : {first_ip}" + "\n")
        txt_hasil.insertPlainText(f"Host Terakhir\t   : {last_ip}" + "\n")
        txt_hasil.insertPlainText(f"Broadcast\t   : {broadcast_add_final}" + "\n")
        txt_hasil.insertPlainText(f"Host Tersedia\t   : {str(no_hosts)}" + "\n")
        txt_hasil.insertPlainText(f"Wildcard mask : {wildcard}")
        txt_hasil.insertPlainText("\n")

    except ValueError:
        txt_hasil.insertPlainText("Tampaknya memasukkan nilai yang salah\n")


def clear_text():
    txt_hasil.clear()


def output():
    clear_text()
    int_octet_ip = 0
    octet_netmask = 0

    input_ip = txt_ip_address.text()
    if cek_input_ip(input_ip):
        int_octet_ip = cek_input_ip(input_ip)
    else:
        txt_hasil.insertPlainText("IP 127 - Digunakan untuk alamat Loopback\n")
        txt_hasil.insertPlainText("IP 169 - Digunakan untuk alamat Link-Local\n")
        txt_hasil.insertPlainText("\n")

    input_netmask = txt_netmask.text()
    if cek_input_netmask(input_netmask):
        octet_netmask = cek_input_netmask(input_netmask)
    else:
        txt_hasil.insertPlainText("Subnet Mask tidak valid, coba lagi.\n")

    if int_octet_ip != 0 and octet_netmask != 0:
        hitung_subnetting(input_ip, input_netmask, int_octet_ip, octet_netmask)
    else:
        txt_hasil.insertPlainText("Anda tampaknya memasukkan nilai yang salah\n")


# GUI
app = QApplication([])
main_window = QMainWindow()
main_window.setGeometry(450, 120, 310, 480)
main_window.setWindowTitle("Aplikasi IP Calculator")
main_window.setWindowIcon(QIcon("icon.png"))

font_judul = QFont()
font_judul.setFamily("Arial")
font_judul.setPointSize(15)
font_judul.setBold(True)
font_judul.setWeight(75)

lbl_judul = QLabel(main_window)
lbl_judul.move(33, 15)
lbl_judul.setFixedWidth(250)
lbl_judul.setText("Subnet Calculator")
lbl_judul.setAlignment(Qt.AlignCenter)
lbl_judul.setFont(font_judul)

font_universal = QFont()
font_universal.setFamily("Arial")
font_universal.setPointSize(10)
font_universal.setBold(False)

lbl_ipv4 = QLabel(main_window)
lbl_ipv4.setFixedWidth(125)
lbl_ipv4.move(20, 50)
lbl_ipv4.setText("IPv4 Network Address")
lbl_ipv4.setFont(font_universal)

lbl_ip_address = QLabel(main_window)
lbl_ip_address.setFixedWidth(125)
lbl_ip_address.move(20, 90)
lbl_ip_address.setText("IP Address")
lbl_ip_address.setFont(font_universal)

txt_ip_address = QLineEdit(main_window)
txt_ip_address.setGeometry(95, 93, 193, 25)
txt_ip_address.setFont(font_universal)

lbl_netmask = QLabel(main_window)
lbl_netmask.setFixedWidth(125)
lbl_netmask.move(20, 122)
lbl_netmask.setText("Netmask")
lbl_netmask.setFont(font_universal)

txt_netmask = QLineEdit(main_window)
txt_netmask.setGeometry(95, 125, 193, 25)
txt_netmask.setFont(font_universal)

txt_hasil = QTextEdit(main_window)
txt_hasil.setGeometry(20, 210, 270, 250)
txt_hasil.setFont(font_universal)
txt_hasil.setReadOnly(True)

btn_hitung = QPushButton(main_window)
btn_hitung.setGeometry(20, 163, 270, 35)
btn_hitung.setText("Hitung")
btn_hitung.setFont(font_universal)
btn_hitung.clicked.connect(output)

main_window.show()
app.exec_()

                                  
