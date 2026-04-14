import rclpy
import serial
from rclpy.node import Node
from std_msgs.msg import String


class UartDriverNode(Node):
    def __init__(self):
        super().__init__("uart_driver_node")

        self.port = "/dev/ttyACM0"
        self.baudrate = 115200

        self.pub = self.create_publisher(String, "uart/read", 10)

        try:
            self.serial_port = serial.Serial(
                port=self.port, baudrate=self.baudrate, timeout=0.01
            )
            self.get_logger().info(
                f"Éxito: Puerto {self.port} abierto a {self.baudrate} bps."
            )
        except serial.SerialException as e:
            self.get_logger().error(f"Fallo fatal al abrir el puerto: {e}")
            return

        self.timer = self.create_timer(0.001, self.read_serial_data)

    def read_serial_data(self):

        if not hasattr(self, "serial_port") or not self.serial_port.is_open:
            return

        if self.serial_port.in_waiting > 0:
            raw_data_line = self.serial_port.readline()

            try:
                # 1. Decodificar los bytes a un string de Python y quitar espacios/saltos de línea
                data_line_str = raw_data_line.decode("utf-8").strip()

                if data_line_str: 
                    msg = String()
                    msg.data = data_line_str
                        
                    self.pub.publish(msg)
                # self.get_logger().info(f"Recibido: {msg.data}") # Descomentar para debug

            except UnicodeDecodeError:
                self.get_logger().warn(
                    "Se recibió basura en el puerto serial (Error de decodificación)."
                )


def main(args=None):
    rclpy.init(args=args)
    node = UartDriverNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Nodo detenido manualmente.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
