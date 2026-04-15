import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32
from robot_interfaces.msg import WheelPositionState
from robot_interfaces.srv import SetWheelPosition

class ProtocolHandlerNode(Node):
    def __init__(self):
        super().__init__("protocol_handler_node")


        self.sub_serial = self.create_subscription(String, "uart/read", self.parse_csv_callback, 10)


        self.pub = self.create_publisher(WheelPositionState, "motor/internal_status", 10)
        
        self.pub_to_uart_node = self.create_publisher(String, "tx_raw_data", 10)

        self.srv_set_position = self.create_service(SetWheelPosition, "hardware/set_position", self.set_position_callback)

        self.get_logger().info("Traductor iniciado. Esperando la telemetría del motor")

        self.ultima_posicion_conocida = 0.0

    def parse_csv_callback(self, msg_out):



        try:

            line = msg_out.data.strip()

            values = line.split(',')


            if len(values) == 4:
               
                setpoint_val = float(values[0])
                posicion_val = float(values[1])
                error_val = float(values[2])
                pwm_val = float(values[3])

                msg_out = WheelPositionState()
                msg_out.setpoint_deg = setpoint_val
                msg_out.position_deg = posicion_val
                msg_out.error_deg = error_val
                msg_out.pid_output = pwm_val
                tiempo_actual = self.get_clock().now().to_msg()
                msg_out.header.stamp.sec = tiempo_actual.sec
                msg_out.header.stamp.nanosec = tiempo_actual.nanosec
                msg_out.header.frame_id = "motor_a_link"

                self.ultima_posicion_conocida = float(values[1])

                self.pub.publish(msg_out)
        except ValueError:
            self.get_logger().warn("Dato corrupto ignorado (no es un número).")
        except Exception as e: 
            self.get_logger().error(f"Error inesperado al traducir: {e}")


    def set_position_callback(self, request, response):
        try:
            # OJO ACÁ: Asegurate de que la variable adentro del archivo .srv se llame "setpoint_deg" o cambiala por el nombre que le hayan puesto.
            nuevo_setpoint = request.position_deg 
            
            # Armamos el comando en texto. (Revisá en app_cli.c si la Pico espera la palabra "SET" o "TARGET", etc)
            comando = f"set set_point {nuevo_setpoint}\n"
            
            # Metemos el texto en el String y lo mandamos a la UART
            msg_uart = String()
            msg_uart.data = comando
            self.pub_to_uart_node.publish(msg_uart)
            
            self.get_logger().info(f"Setpoint de {nuevo_setpoint} recibido de Maxi y mandado a la Pico.")

            # Llenamos la respuesta (el acuse de recibo) para Maxi
            response.success = True
            response.message = "Comando enviado a la UART exitosamente."
            
        except Exception as e:
            response.success = False
            response.message = f"Error al procesar el setpoint: {e}"
            self.get_logger().error(response.message)

        return response

def main(args=None):
    rclpy.init(args=args)
    node = ProtocolHandlerNode()
    try: 
        rclpy.spin(node)
    except KeyboardInterrupt: 
        node.get_logger().info("Traductor detenido manualmente.")
    finally:
        node.destroy_node()
        rclpy.shutdown()
if __name__ == "__main__":
    main()    


                


