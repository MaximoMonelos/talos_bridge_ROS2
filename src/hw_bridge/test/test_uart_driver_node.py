import pytest
import rclpy
from rclpy.executors import SingleThreadedExecutor
from std_msgs.msg import ByteMultiArray
from unittest.mock import patch, MagicMock

# TDD: Esta importación fallará hasta que crees el archivo y la clase.
# Asegúrate de crear el nodo 'UartDriverNode' en 'hw_interface/uart_driver_node.py'
from hw_bridge.uart_driver import UartDriverNode


@pytest.fixture(scope="module")
def ros2_lifecycle():
    """Fixture para inicializar y apagar ROS2 de manera limpia."""
    rclpy.init()
    yield
    rclpy.shutdown()


@pytest.fixture
def mock_serial_port():
    """Fixture que devuelve un mock de pyserial para evitar acceso a hardware real."""
    with patch('serial.Serial') as mock_serial:
        # Configuramos el mock para que simule una conexión exitosa
        instance = mock_serial.return_value
        instance.is_open = True
        yield instance


class TestUartDriverNode:
    """Suite de pruebas TDD para el driver UART aislado."""

    def test_node_initialization(self, ros2_lifecycle, mock_serial_port):
        """Verifica que el nodo se crea y abre el puerto serial configurado."""
        node = UartDriverNode(port='/dev/ttyMock', baudrate=115200)
        
        # El nodo debería haber intentado abrir el puerto con pyserial
        mock_serial_port.close.assert_not_called()
        assert node.get_name() == 'uart_driver_node'
        node.destroy_node()

    def test_tx_ros2_to_uart(self, ros2_lifecycle, mock_serial_port):
        """
        Verifica que un mensaje recibido en el tópico 'serial_tx' 
        se escriba directamente en el buffer de pyserial.
        """
        node = UartDriverNode(port='/dev/ttyMock')
        executor = SingleThreadedExecutor()
        executor.add_node(node)

        # Simulamos un publicador temporal para enviar datos al nodo
        pub = node.create_publisher(ByteMultiArray, 'serial_tx', 10)
        
        # Preparamos el mensaje de prueba (trama cruda simulada)
        test_msg = ByteMultiArray()
        test_msg.data = [0xAA, 0x01, 0x05, 0xBB] # Ej: Start, CMD, Val, End
        
        # Publicamos y damos tiempo al executor para procesar el callback
        pub.publish(test_msg)
        executor.spin_once(timeout_sec=0.1)

        # Verificamos que el nodo llamó a serial.write con los bytes exactos
        mock_serial_port.write.assert_called_once_with(bytes([0xAA, 0x01, 0x05, 0xBB]))
        
        node.destroy_node()

    def test_rx_uart_to_ros2(self, ros2_lifecycle, mock_serial_port):
        """
        Verifica que los datos pendientes en el buffer de pyserial
        se lean y se publiquen en el tópico 'serial_rx'.
        """
        node = UartDriverNode(port='/dev/ttyMock')
        executor = SingleThreadedExecutor()
        executor.add_node(node)

        # Configuramos el mock para simular que hay bytes esperando ser leídos
        mock_serial_port.in_waiting = 4
        mock_serial_port.read.return_value = bytes([0xCC, 0x02, 0x08, 0xDD])

        # Creamos una bandera y un subscriptor temporal para capturar la salida del nodo
        received_data = []
        def rx_callback(msg):
            received_data.extend(msg.data)
            
        sub = node.create_subscription(ByteMultiArray, 'serial_rx', rx_callback, 10)

        # Forzamos la ejecución. El temporizador interno del nodo (ej. a 100Hz) 
        # debería dispararse y procesar la lectura serial.
        executor.spin_once(timeout_sec=0.1)

        # Verificamos que se leyó el hardware simulado
        mock_serial_port.read.assert_called_once()
        
        # Verificamos que ROS2 recibió la trama encapsulada
        assert received_data == [0xCC, 0x02, 0x08, 0xDD], "El nodo no publicó los bytes correctos en serial_rx"

        node.destroy_node()