import rclpy
from rclpy.node import Node
from std_msgs.msg import String # Importamos el tipo de mensaje de texto estándar

class NodoPublicador(Node):
    def __init__(self):
        # Iniciamos el nodo con el nombre 'mi_nodo_publicador'
        super().__init__('foro_maxi')
        
        # CREAMOS EL TOPIC aquí. 
        # Tipo de mensaje: String, Nombre del topic: 'mensaje_husarnet', Tamaño de cola: 10
        self.publisher_ = self.create_publisher(String, 'mensaje_husarnet', 10)
        
        # Creamos un temporizador que ejecutará una función cada 1 segundo (1.0)
        timer_period = 1.0  
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.contador = 0

    def timer_callback(self):
        # Esta función se llama cada segundo
        msg = String() # Creamos el objeto del mensaje
        msg.data = f'¡Hola desde mi PC! Mensaje número: {self.contador}' # Le asignamos el texto
        
        self.publisher_.publish(msg) # MANDAMOS EL MENSAJE AL TOPIC
        
        # Mostramos en la consola lo que estamos mandando para comprobar
        self.get_logger().info(f'Publicando: "{msg.data}"') 
        self.contador += 1

def main(args=None):
    rclpy.init(args=args)
    nodo_pub = NodoPublicador()
    
    try:
        rclpy.spin(nodo_pub) # Mantiene el nodo corriendo
    except KeyboardInterrupt:
        pass
    
    # Cuando lo detenemos (Ctrl+C), cerramos todo limpiamente
    nodo_pub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()