from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    # 1. Nodo de interfaz con hardware/simulación (ej. Webots)
    bridge_node_motor_status = Node(
        package="ia_bridge",  # Nombre de tu paquete
        executable="motor_status_node",  # Nombre del ejecutable definido en CMakeLists/setup.py
        name="ia_bridge",  # Nombre del nodo en tiempo de ejecución
        output="screen",
    )

    bridge_node_motor_set = Node(
        package="ia_bridge",
        executable="motor_service_node",
        name="ia_brain",
        output="screen",
    )

    brain_node = Node(
        package="autonomous_rover_brain",
        executable="langchain_node",
        name="ia_brain",
        output="screen",
    )

    motor_uart_node = Node(
        package="hw_bridge",
        executable="uart_driver_node",
        name="uart_driver",
        output="screen",
    )

    motor_protocol_handler = Node(
        package="hw_bridge",
        executable="protocol_handler_node",
        name="protocol_handler",
        output="screen",
    )



    # Útil si estás usando herramientas basadas en TUI
    # teleop_node = Node(
    #     package='teleop_twist_keyboard',
    #     executable='teleop_twist_keyboard',
    #     name='teleop',
    #     output='screen',
    #     prefix='xterm -e'               # Abre una nueva ventana de terminal para este nodo
    # )

    # La función debe retornar un objeto LaunchDescription con las acciones a ejecutar
    return LaunchDescription(
        [bridge_node_motor_status, bridge_node_motor_set, brain_node, motor_uart_node, motor_protocol_handler]
    )
