import rclpy
from rclpy.logging import LoggingSeverity
from rclpy.node import Node

# Importamos TU mensaje compilado
from robot_interfaces.msg import WheelPositionState


class PositionPublisherMock(Node):
    def __init__(self):
        super().__init__("position_publisher_mock")

        self.get_logger().set_level(LoggingSeverity.DEBUG)
        # Creamos el publicador
        self.publisher_ = self.create_publisher(
            WheelPositionState, "/talos/rueda_delantera_izq/posicion", 10
        )

        # Publicamos a 2 Hz (cada 0.5 segundos)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.get_logger().info("Nodo de prueba de posición iniciado...")

        # Variable para simular que la rueda gira
        self.pos_simulada = 0.0

    def timer_callback(self):
        msg = WheelPositionState()

        # 1. Llenamos el Header (Marca de tiempo y marco de referencia)
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "rueda_delantera_izq_link"

        # 2. Llenamos los datos principales
        msg.wheel_id = "rueda_delantera_izq"
        msg.position_deg = self.pos_simulada
        msg.is_online = True

        # 3. Llenamos el resto con datos inventados para que se vean en el 'echo'
        msg.position_deg_rel = 5.0
        msg.setpoint_deg = 360.0
        msg.error_deg = msg.setpoint_deg - msg.position_deg
        msg.pid_output = 0.75
        msg.duty_cycle = 0.8

        # Lógica de simulación (sumar 5 grados)
        self.pos_simulada += 5.0
        if self.pos_simulada >= 360.0:
            self.pos_simulada = 0.0

        self.publisher_.publish(msg)
        self.get_logger().debug(f"Publicando posición: {msg.position_deg} grados")


def main(args=None):
    rclpy.init(args=args)
    node = PositionPublisherMock()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
