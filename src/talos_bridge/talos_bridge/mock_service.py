import rclpy
from rclpy.node import Node

# ¡Importamos tu servicio!
from robot_interfaces.srv import SetWheelPosition


class PositionServiceMock(Node):
    def __init__(self):
        super().__init__("position_service_mock")

        self.srv = self.create_service(
            SetWheelPosition, "talos/set_wheel_position", self.set_position_callback
        )

        self.get_logger().info(
            "Mock del Servicio SetWheelPosition iniciado y esperando comandos..."
        )

    def set_position_callback(self, request, response):
        # 1. Leemos lo que nos pide el cliente (request)
        rueda = request.wheel_id
        posicion_deseada = (
            request.position_deg
        )  # Asegurate de que esto coincida con tu .srv

        self.get_logger().info(
            f'¡Orden recibida! Moviendo rueda "{rueda}" a {posicion_deseada} grados.'
        )

        # 2. Acá iría la comunicación real con tu micro
        # En el futuro, acá empaquetarías los bytes por serial hacia la Pico.
        # Por ahora, simulamos que la Pico hizo el trabajo en 0.1 segundos y respondió OK.

        # 3. Llenamos la respuesta (response) para devolvérsela al que llamó
        response.success = True
        response.message = (
            f"Comando enviado y aceptado por la Raspberry Pi Pico para {rueda}"
        )
        response.final_position_deg = (
            posicion_deseada  # Simulamos que llegó perfecto a la meta
        )

        return response


def main(args=None):
    rclpy.init(args=args)
    node = PositionServiceMock()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
