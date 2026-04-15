import rclpy
import serial
from rclpy.logging import LoggingSeverity
from rclpy.node import Node
from std_msgs.msg import String


class UartDriverNode(Node):
    def __init__(self):
        super().__init__("uart_driver_node")

        self.get_logger().set_level(LoggingSeverity.DEBUG)

        self.port = "/dev/ttyACM0"
        self.baudrate = 115200

        self.sub_to_pico = self.create_subscription(String, "tx_raw_data", self.write_serial_callback, 10)

        self.pub = self.create_publisher(String, "uart/read", 10)

        try:
            self.serial_port = serial.Serial(
                port=self.port, baudrate=self.baudrate, timeout=0.01
            )
            self.get_logger().info(
                f"Éxito: Puerto {self.port} abierto a {self.baudrate} bps."
            )
        except serial.SerialException as e:
            self.get_logger().fatal(f"Fallo fatal al abrir el puerto: {e}")
            return

        self.timer = self.create_timer(0.001, self.read_serial_data)

    def read_serial_data(self):

        if not hasattr(self, "serial_port") or not self.serial_port.is_open:
            return

        if self.serial_port.in_waiting > 0:
            raw_data_line = self.serial_port.readline()
            self.get_logger().debug(
                f"→ Datos seriales recibidos, length={len(raw_data_line)}: {raw_data_line}"
            )

            try:
                # 1. Decodificar los bytes a un string de Python y quitar espacios/saltos de línea
                data_line_str = raw_data_line.decode("utf-8").strip()
                self.get_logger().debug(f"→ Decodificado: '{data_line_str}'")

                if data_line_str:
                    msg = String()
                    msg.data = data_line_str

                    self.pub.publish(msg)
                    self.get_logger().debug(
                        f"→ Publicando a tópicos: '{msg.data}'"
                    )

            except UnicodeDecodeError:
                self.get_logger().warn("Se recibió basura en el puerto serial (Error de decodificación).")

    def write_serial_callback(self, msg):

        if not hasattr(self, "serial_port") or not self.serial_port.is_open:
            self.get_logger().warn("Intentando mandar un comando pero el puerto esta cerrado")
            return 
        try:
            comando_bytes = msg.data.encode('utf-8')

            self.serial_port.write(comando_bytes)

            self.get_logger().info(f"Comando enviado a la UART: {msg.data.strip()}")
        except Exception as e:
            self.get_logger().error(f"Exploto la escritura en el serial: {e}")



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
