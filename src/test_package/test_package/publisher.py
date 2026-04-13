import rclpy
from rclpy.node import Node

from std_msgs.msg import String  # Importamos el tipo de mensaje de texto estándar


class NodoPublicador(Node):

    def __init__(self):
        # Le ponemos nombre al nodo
        super().__init__('mi_primer_nodo')

        # CREAMOS EL TOPIC aquí.
        # 1. Tipo de mensaje (String)
        # 2. Nombre del canal ('mensaje_chat')
        # 3. Tamaño de la "cola" de mensajes (10)
        self.publisher_ = self.create_publisher(String, 'mensaje_chat', 10)

        # Configuramos un TIMER para que el nodo haga algo cada cierto tiempo
        timer_period = 1.0
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Contador de mensajes
        self.contador = 0

    def timer_callback(self):
        msg = String()  # Creamos el objeto del mensaje
        msg.data = f'¡Hola desde mi PC! Mensaje número: {self.contador}'  # Le asignamos el texto

        self.publisher_.publish(msg)  # MANDAMOS EL MENSAJE AL TOPIC

        self.get_logger().info(f'Publicando: "{msg.data}"')
        self.contador += 1


def main(args=None):
    rclpy.init(args=args)

    nodo_pub = NodoPublicador()

    try:
        rclpy.spin(nodo_pub)  # Mantiene el nodo corriendo
    except KeyboardInterrupt:
        pass
    finally:
        nodo_pub.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
