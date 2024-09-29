import logging
import socket
import re

import pyfiglet
from rich import print as banner


logging.basicConfig(
    filename='server.log', 
    filemode='a', 
    format='%(asctime)s - %(levelname)s - SERVER %(message)s', 
    level=logging.INFO
)


def validate_data(data):
    """
    Validate data which is name, email, 
    phone number, and age before saving.
    """
    data_list = data.strip().split(',')

    if len(data_list) != 4:
        return False

    name, email, phone_number, age = data_list
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    phone_number_regex = r'^(\d{11}|\d{12})$'

    if not re.match(email_regex, email) or not re.match(phone_number_regex, phone_number):
        return False

    if not age.isdigit():
        return False

    if not isinstance(name, str) or name.isdigit():
        return False

    return True


def save_data(data):
    """Appends a new data line to the file."""
    with open("data_received.txt", "a") as f:
        f.write(data)


def tcp_ip_server():
    """
    Create a continuous data reception 
    service that uses TCP/IP protocol
    """
    logging.info("Iniciando servidor TCP/IP...")
    PORT = 5784
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', PORT))
    server.listen(5)
    logging.info("Servidor rodando na porta 5784")
    banner(pyfiglet.figlet_format('Nimbus\nMeteorologia', font='big', width=300))
    print("Servidor TCP/IP rodando na porta 5784. Aguardando conexões...")
    logging.info("Aguardando conexões...")

    try:
        while True:
            client_socket, client_address = server.accept()
            logging.info(f"Conexão recebida de {client_address}")
            print(f"Conexão recebida de {client_address}")

            data_received = client_socket.recv(1024).decode('utf-8')
            logging.info("-" * 20)
            logging.info(f"Dados recebidos: {data_received}")

            if data_received:
                if validate_data(data_received):
                    save_data(data_received)
                    logging.info("Dados válidos e salvos!")
                    logging.info("-" * 20)
                    client_socket.sendall("Ok".encode('utf-8'))
                else:
                    logging.error("Dados inválidos!")
                    client_socket.sendall("Erro: formato inválido".encode('utf-8'))

            client_socket.close()
    except KeyboardInterrupt:
        logging.info("Servidor interrompido manualmente.")
        print("\nServidor interrompido manualmente.")
    except Exception as e:
        logging.critical(f"Ocorreu o seguinte erro no servidor: {e}")
    finally:
        logging.info("Servidor interrompido.")
        server.close()


if __name__ == "__main__":
    tcp_ip_server()
