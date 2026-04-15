#!/usr/bin/env python3

import sys
import rclpy
from rclpy.node import Node

# Importamos el servicio custom que creaste
from robot_interfaces.srv import Chat

class ChatClient(Node):
    def __init__(self):
        super().__init__('chat_terminal_client')
        # Creamos el cliente apuntando al mismo tipo y nombre de servicio
        self.cli = self.create_client(Chat, '/chat')
        
        # Esperamos a que el servicio esté en línea antes de arrancar
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Buscando la red neuronal... esperando al servicio /chat.')
            
        self.req = Chat.Request()

    def send_request(self, prompt_text):
        # Asignamos el texto al request
        self.req.prompt = prompt_text
        
        # Hacemos la llamada asíncrona
        self.future = self.cli.call_async(self.req)
        
        # Bloqueamos este hilo hasta que el servicio responda
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    chat_client = ChatClient()

    print("\n" + "="*50)
    print("🤖 Conexión establecida con el cerebro de Talos 🤖")
    print("Escribí tu mensaje y presioná Enter.")
    print("Escribí 'salir', 'exit' o presioná Ctrl+C para terminar.")
    print("="*50 + "\n")

    try:
        while True:
            # Capturamos el input del usuario en la terminal
            user_input = input("\033[94mUsuario:\033[0m ") # \033[94m le da color azul en consola
            
            if user_input.lower() in ['salir', 'exit', 'quit']:
                print("\nDesconectando...")
                break

            if not user_input.strip():
                continue

            # Enviamos el request y esperamos
            response = chat_client.send_request(user_input)
            
            # Imprimimos la respuesta del agente
            print(f"\033[92mTalos:\033[0m {response.reply}\n") # \033[92m le da color verde
            
    except KeyboardInterrupt:
        print("\nDesconectando por interrupción del usuario...")
    finally:
        chat_client.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()