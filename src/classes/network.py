import socket, threading, json

class NetPeer:
    def __init__(self):
        self.sock = None
        self.connected = None
        self.alive = threading.Event()
        self.alive.set()
        self.lock = threading.Lock()
        
        self.player_join_event = None

    def host(self, port=5432):
        host_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host_sock.bind(('', port))
        host_sock.listen(1)
        self.sock = host_sock

        def accept_loop():
            try:
                self.connected, addr = self.sock.accept()
                self.connected.settimeout(0.1)
                self._recv_loop(self.connected)
            except Exception as e:
                print(f"Error accepting connection: {e}")
            finally:
                self.close()
        threading.Thread(target=accept_loop, daemon=True).start()
    
    def join(self, ip, port=5432):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.settimeout(0.1)
        self.sock = client
        threading.Thread(target=self._recv_loop, args=(self.sock,), daemon=True).start()

    def send(self, obj:dict):
        data = (json.dumps(obj) + '\n').encode('utf-8')
        try:
            with self.lock:
                s = self.connected if self.connected else self.sock
                if not s:
                    return
                s.sendall(data)
        except Exception as e:
            print(f"Error sending data: {e}")

    def _recv_loop(self, s:socket.socket):
        buff = b""
        try: 
            while self.alive.is_set():
                try:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    buff += chunk
                    while b'\n' in buff:
                        line, buff = buff.split(b'\n', 1)
                        if not line:
                            continue
                        try:
                            msg = json.loads(line.decode('utf-8'))
                            if self.on_message:
                                self.on_message(msg)
                        except Exception as e:
                            print(f"Error processing message: {e}")
                except socket.timeout:
                    pass
        except Exception as e:
            print(f"Error receiving data: {e}")
        finally:
            self.close()

    def close(self):
        self.alive.clear()
        try:
            if self.connected:
                self.connected.close()
            if self.sock:
                self.sock.close()
        except Exception as e:
            print(f"Error closing socket: {e}")

    def on_message(self, msg):
        print("message recieved:", msg)
        match msg["type"]:
            case "join":
                self.player_join_event = msg['content']
            case "host_name":
                print(f"Host name received: {msg['content']}")
                self.player_join_event = msg['content']
            case _:
                print(f"Unknown message type: {msg['type']}")

    def get_player_join_event(self):
        if self.player_join_event is not None:
            event = self.player_join_event
            self.player_join_event = None
            return event
    
        return None
