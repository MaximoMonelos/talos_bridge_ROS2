# Talos SN Workspace

Este repositorio contiene el espacio de trabajo de ROS 2 para el proyecto **Talos**, diseñado como la rama central encargada de realizar las conexiones entre las herramientas de un **agente de IA** y el **hardware** robótico.

## Propósito del Proyecto

Talos SN (Sensor Network) actúa como un puente (bridge) de comunicación. Permite que un agente inteligente envíe comandos de alto nivel (como posicionar una rueda o ajustar ganancias PID) y reciba retroalimentación del estado de los sensores en tiempo real, abstrayendo la complejidad de los protocolos serie o de bajo nivel.

## Estructura del Espacio de Trabajo

El workspace está compuesto por los siguientes paquetes principales:

### 1. `robot_interfaces`
Contiene todas las definiciones de mensajes, servicios y acciones personalizadas necesarias para el control del robot:
*   **Mensajes (`msg`):** `PIDGains`, `WheelPositionState`, `WheelVelocityState`.
*   **Servicios (`srv`):** `SetWheelPosition`, `SetWheelVelocity`, `GetPIDGains`, etc.
*   **Acciones (`action`):** `DriveWheelPosition`, `DriveWheelVelocity`.

### 2. `talos_bridge`
Es el paquete encargado de la lógica de conexión. Actualmente cuenta con implementaciones de prueba (mocks) que simulan la interacción con el hardware (ej. Raspberry Pi Pico):
*   `mock_position.py`: Publica estados simulados de la posición de las ruedas.
*   `mock_service.py`: Emula un servicio que acepta comandos de posicionamiento y confirma su recepción.

### 3. `test_package`
Un paquete auxiliar para pruebas básicas y validación de publicadores.

## Requisitos

*   [ROS 2 (Humble/Iron/Jazzy)](https://docs.ros.org/en/humble/Installation.html)
*   Python 3
*   Colcon (herramienta de construcción)

## Instalación y Construcción

1.  Clona el repositorio en tu espacio de trabajo:
    ```bash
    mkdir -p ~/talos_ws/src
    cd ~/talos_ws/src
    # git clone <url-del-repo> .
    ```

2.  Instala las dependencias:
    ```bash
    cd ~/talos_ws
    rosdep install -i --from-path src --rosdistro $ROS_DISTRO -y
    ```

3.  Construye el workspace:
    ```bash
    colcon build --symlink-install
    ```

4.  Carga el entorno:
    ```bash
    source install/setup.bash
    ```

## Uso

Para probar la comunicación simulada:

1.  **Lanzar el servicio mock:**
    ```bash
    ros2 run talos_bridge mock_service
    ```

2.  **Lanzar el publicador de posición mock:**
    ```bash
    ros2 run talos_bridge mock_position
    ```

3.  **Enviar un comando desde la terminal:**
    ```bash
    ros2 service call /talos/set_wheel_position robot_interfaces/srv/SetWheelPosition "{wheel_id: 'rueda_delantera_izq', position_deg: 90.0}"
    ```

Para ejecutar el proyecto:

```bash
ros2 launch talos_bridge talos_start.launch.py
```

---
**Desarrollado para la integración de IA y Robótica.**
