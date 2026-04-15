import rclpy
from rclpy.logging import LoggingSeverity
from rclpy.node import Node

from robot_interfaces.msg import WheelPositionState


class TopicsNode(Node):
    def __init__(self):
        super().__init__("motor_topic_node")

        self.get_logger().set_level(LoggingSeverity.DEBUG)
        # 1. DECLARAR EL PARÁMETRO
        # El primer argumento es la ruta exacta dentro del YAML.
        # El segundo argumento es el valor por defecto en caso de que el YAML no se cargue.
        self.declare_parameter("topics.publishers.status", "motor/position_state")
        self.declare_parameter("publish_frequency", 10.0)  # Frecuencia en Hz

        topic_name = (
            self.get_parameter("topics.publishers.status")
            .get_parameter_value()
            .string_value
        )
        frequency = (
            self.get_parameter("publish_frequency").get_parameter_value().double_value
        )
        # 3. USAR EL VALOR PARA CREAR EL PUBLICADOR
        self.pub = self.create_publisher(WheelPositionState, topic_name, 10)

        if frequency <= 0:
            self.get_logger().fatal(
                f"Frecuencia de publicación inválida: {frequency}Hz. Debe ser > 0."
            )
            raise ValueError("Frecuencia inválida")

        self.get_logger().debug(
            f"Configuración cargada - Tópico: {topic_name}, Frecuencia: {frequency}Hz"
        )

        self.timer = self.create_timer((1 / frequency), self.timer_callback)

        # Opcional: Imprimir en consola para verificar que cargó bien
        self.get_logger().info(f"Publicando en: {topic_name} a {frequency}Hz")

        self.fake_position = 0.0

    def timer_callback(self):
        msg = WheelPositionState()

        msg.header.stamp = self.get_clock().now().to_msg()

        self.fake_position += 0.01

        msg.position_deg = self.fake_position

        self.pub.publish(msg)
        self.get_logger().debug(f"Publicada posición simulada: {msg.position_deg:.2f}°")


def main(args=None):
    rclpy.init(args=args)
    node = TopicsNode()
    try:
        rclpy.spin(node)  # El spin mantiene el nodo vivo y atendiendo al timer
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
