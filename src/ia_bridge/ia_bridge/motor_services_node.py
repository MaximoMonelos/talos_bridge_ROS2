import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.logging import LoggingSeverity
from rclpy.node import Node

from robot_interfaces.srv import SetWheelPosition


class ServiceNode(Node):
    def __init__(self):
        super().__init__("motor_service_node")

        self.get_logger().set_level(LoggingSeverity.DEBUG)
        self.group = ReentrantCallbackGroup()

        self.srv = self.create_service(
            SetWheelPosition,
            "motor/set_position",
            self.position_callback,
            callback_group=self.group,
        )

        self.hw_client = self.create_client(
            SetWheelPosition, "hardware/set_position", callback_group=self.group
        )
        self.get_logger().info("Servicio de Posición listo para recibir peticiones.")

    async def position_callback(self, request, response):
        self.get_logger().info(
            f"Petición de la Tool: Rueda {request.wheel_id} a {request.position_deg}°"
        )

        if not self.hw_client.wait_for_service(timeout_sec=1.0):
            response.success = False
            response.message = "Error: El protocol_handler no responde."
            return response

        if request.position_deg > 360.0:
            response.success = False
            response.message = "Error: Fuera de rango."
            return response

        hw_request = SetWheelPosition.Request()
        hw_request.wheel_id = request.wheel_id
        hw_request.position_deg = request.position_deg

        self.get_logger().info("Esperando respuesta del hardware...")
        try:
            # Llamamos al hardware y esperamos la respuesta de forma asíncrona
            hw_result = await self.hw_client.call_async(hw_request)

            # Si llegamos acá, es porque el protocol_handler ya recibió el ACK de la UART
            response.success = hw_result.success
            response.message = f"Hardware confirmó: {hw_result.message}"

        except Exception as e:
            response.success = False
            response.message = f"Fallo en la comunicación interna: {str(e)}"

        return response


def main(args=None):
    rclpy.init(args=args)
    node = ServiceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
