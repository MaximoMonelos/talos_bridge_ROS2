import rclpy
from rclpy.logging import LoggingSeverity
from rclpy.node import Node

from robot_interfaces.srv import SetWheelPosition


class HardwareMock(Node):
    def __init__(self):
        super().__init__("hardware_mock_node")
        # Creamos el servicio que tu ia_bridge está buscando

        self.get_logger().set_level(LoggingSeverity.DEBUG)

        self.srv = self.create_service(
            SetWheelPosition, "hardware/set_position", self.callback
        )
        self.get_logger().info("Mock de Hardware (Pico) esperando comandos...")

    def callback(self, request, response):
        self.get_logger().info(
            f"Comando recibido para rueda {request.wheel_id}: {request.position_deg} grados"
        )
        self.get_logger().debug(
            f"Simulando procesamiento interno para rueda {request.wheel_id}..."
        )

        # Simulamos que todo salió bien
        response.success = True
        response.message = "ACK desde la Raspberry Pi Pico"
        return response


def main():
    rclpy.init()
    node = HardwareMock()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()


if __name__ == "__main__":
    main()
