# Versão Final

import socket
import os
import sys
import time

# Identificação
NODES_CONFIG = {
    "1": {"port": 5001, "folder": "Nodo1/arquivos_sincronizados/"},
    "2": {"port": 5002, "folder": "Nodo2/arquivos_sincronizados/"},
    "3": {"port": 5003, "folder": "Nodo3/arquivos_sincronizados/"},
    "4": {"port": 5004, "folder": "Nodo4/arquivos_sincronizados/"}
}
HOST = "127.0.0.1"
BUFFER_SIZE = 65536

# Funções auxiliares do código

def get_node_id():
    if len(sys.argv) < 2 or sys.argv[1] not in NODES_CONFIG:
        print(f"ERRO: Especifique um ID de nodo válido ({', '.join(NODES_CONFIG.keys())})")
        sys.exit(1)
    return sys.argv[1]

def create_socket(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, port))
    sock.setblocking(False)
    print(f"Servidor UDP escutando em {HOST}:{port}")
    return sock

def get_peers(my_id):
    return [(HOST, cfg["port"]) for node_id, cfg in NODES_CONFIG.items() if node_id != my_id]

# Funções de lógica do código

def check_folder_changes(folder_path, known_files, peers, sock):
    """Verifica a pasta por arquivos novos ou removidos e notifica os peers."""
    try:
        current_files = set(os.listdir(folder_path))
    except FileNotFoundError:
        print(f"AVISO: Diretório '{folder_path}' não encontrado. Criando...")
        os.makedirs(folder_path)
        current_files = set()

    # Loop de verificação de arquivos adicionados
    new_files = current_files - known_files
    for filename in new_files:
        filepath = os.path.join(folder_path, filename)
        try:
            with open(filepath, 'rb') as f:
                file_content = f.read()
            
            message = b'NOVO:' + filename.encode('utf-8') + b':' + file_content
            print(f"Detectado novo arquivo: {filename}. Enviando para os peers...")
            for peer in peers:
                sock.sendto(message, peer)
        except IOError as e:
            print(f"Erro ao ler o novo arquivo {filename}: {e}")

    # Loop de verificação de arquivos removidos
    removed_files = known_files - current_files
    for filename in removed_files:
        message = f"REMOVE:{filename}".encode('utf-8')
        print(f"Detectado arquivo removido: {filename}. Notificando os peers...")
        for peer in peers:
            sock.sendto(message, peer)
            
    return current_files

def process_received_data(data, folder_path):
    """Processa uma mensagem recebida de um peer."""
    try:
        header, content = data.split(b':', 1)
        
        if header == b'ONLINE':
            print(f"Peer {content.decode('utf-8')} está online.")
            return

        filename_bytes, file_content = content.split(b':', 1)
        filename = filename_bytes.decode('utf-8')
        filepath = os.path.join(folder_path, filename)

        if header == b'NOVO':
            print(f"Recebendo arquivo '{filename}'...")
            with open(filepath, 'wb') as f:
                f.write(file_content)
            print(f"Arquivo '{filename}' salvo com sucesso.")
        
    except ValueError:
        header, filename_bytes = data.split(b':', 1)
        filename = filename_bytes.decode('utf-8')
        filepath = os.path.join(folder_path, filename)

        if header == b'REMOVE':
            if os.path.exists(filepath):
                print(f"Recebendo instrução para remover '{filename}'...")
                os.remove(filepath)
                print(f"Arquivo '{filename}' removido com sucesso.")
            else:
                print(f"Instrução para remover '{filename}', mas ele não existe localmente.")

# Função principal

def main():
    my_id = get_node_id()
    my_config = NODES_CONFIG[my_id]
    sock = create_socket(my_config["port"])
    peers = get_peers(my_id)
    my_folder = my_config["folder"]

    print(f"Nodo {my_id} iniciado. Pasta: ./{my_folder}")

    # Estado inicial
    known_files = set()
    try:
        known_files = set(os.listdir(my_folder))
    except FileNotFoundError:
        os.makedirs(my_folder)

    last_check = time.time()

    while True:
        # Processar mensagens recebidas
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            print(f"\n--- Mensagem recebida de {addr} ---")
            process_received_data(data, my_folder) 
            known_files = set(os.listdir(my_folder))
            print("----------------------------------")
        except BlockingIOError:
            pass

        # Verificar mudanças na pasta a cada 5 segundos
        if time.time() - last_check > 5:
            known_files = check_folder_changes(my_folder, known_files, peers, sock)
            last_check = time.time()
        
        time.sleep(0.1) # Ppara evitar uso excessivo de CPU

if _name_ == "_main_":
    main()
