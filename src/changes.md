# Registro de Cambios

## [14/04/2026] - 11:32am

### Nuevas Incorporaciones:

- **ia_bridge**: Implementación robusta del sistema de gestión para motores.
    - **Tópicos (`motor_topics_node.py`)**: Integración del sistema de parámetros de ROS 2. Ahora consume configuraciones dinámicas desde `config.yaml` para el nombre del tópico (`motor/status`) y frecuencia (`10.0Hz`). Incluye simulación de telemetría.
    - **Servicios (`motor_services_node.py`)**: Implementación del servidor para `SetWheelPosition`. Incluye validación de rango físico (-360 a 360 grados) y republicación de comandos hacia un tópico interno de control.
- **hw_bridge**: Puente de comunicación hardware avanzado.
    - **`uart_driver.py`**: Evolución del driver serial. Se implementó un sistema de lectura asíncrona mediante un `timer` (0.001s) para procesar datos entrantes. 
    - Se agregó un publicador en el tópico `uart/read` para distribuir la información recibida desde el hardware.
    - Ajuste de configuración para Linux: se cambió el puerto por defecto a `/dev/ttyACM0` y se añadió manejo de errores de decodificación UTF-8 para ignorar datos corruptos.
- **robot_interfaces (Mensajería Interna)**: 
    - Se creó `InternalPositionData.msg` para el pasaje de comandos validados entre el bridge de IA y los controladores de bajo nivel.

### Modificaciones:

- **robot_interfaces**: Optimización de la interfaz pública y configuración de build.
    - **`WheelPositionState.msg`**: Se eliminaron los campos `position_deg_rel` y `duty_cycle` para simplificar la telemetría externa.
    - **`CMakeLists.txt`**: Actualización de la generación de interfaces para incluir los nuevos mensajes y asegurar la compatibilidad con el sistema de build `rosidl`.
- **talos_bridge**: Refactorización técnica y estandarización.
    - Aplicación de PEP 8 y unificación de estilo de comillas en los nodos de simulación `mock_position.py` y `mock_service.py`.
    - Mejora en la lógica de respuesta de los mocks para reflejar mejor el comportamiento esperado de la Raspberry Pi Pico.
