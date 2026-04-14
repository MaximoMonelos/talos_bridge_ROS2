import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from robot_interfaces.srv import SetWheelPosition
from robot_interfaces.msg import InternalPositionData

class ServiceNode(Node):
    def __init__(self):
        super().__init__("motor_service_node")

        self.group = ReentrantCallbackGroup()

        self.srv = self.create_service(
            SetWheelPosition, "motor/set_position", self.position_callback
        )

        self.internal_pub = self.create_publisher(
            InternalPositionData, "motor/internal_position_data", 10
        )

        self.get_logger().info("Servicio de Posición listo para recibir peticiones.")

    def position_callback(self, request, response):

        target_deg = request.position_deg
        target_wheel = request.wheel_id

        self.get_logger().info(f"Petición recibida: Mover a {target_deg}")

        if target_deg > 360 or target_deg < -360:
            response.success = False
            response.message = "Error: Posición fuera de rango físico (-360 a 360)."
            self.get_logger().warn(f"Validación fallida para: {target_deg}")
            return response

        internal_message = InternalPositionData()
        internal_message.wheel_id = target_wheel
        internal_message.position_deg = target_deg

        self.internal_pub.publish(internal_message)

        # Falta que nos llegue la posicion final de otro lado, nose si usar un service definir
        response.success = True
        response.message = f"Posición {target_deg} validada y enviada al controlador."

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
