# Registro de Cambios

## [15/04/2026] - Mejoras de Observabilidad y Testing

### Mejoras de Observabilidad (Logs):

- **hw_bridge (`uart_driver.py`)**: 
    - Cambio a log nivel `fatal` si falla la apertura del puerto serial. 
    - Implementación de logs `debug` para la traza de datos recibidos y mensajes decodificados.
    - Captura de excepciones generales en la lectura con log `error`.
- **ia_bridge**:
    - **`motor_services_node.py`**: Inserción de logs `error` cuando falla el callback del servicio (fuera de rango o timeout) y uso de `debug` para trazar la llamada asíncrona al hardware.
    - **`motor_topics_node.py`**: Validación de la frecuencia de publicación con log `fatal` en caso de valores inválidos (<= 0). Las publicaciones periódicas ahora se loguean en `debug`.
- **talos_bridge (`mock_position.py` y `mock_service.py`)**:
    - Reducción de los logs periódicos de `info` a `debug` para evitar saturación de la terminal.
    - Se agregó una validación simulada en `mock_service.py` que emite un `warning` si se solicita una posición > 360°.

### Testing y Simulaciones:

- **test_package (`hardware_mock.py` y `publisher.py`)**: 
    - Ajuste de salida pasando logs de rutina a `debug` para facilitar las pruebas del `motor_services_node.py` y mantener la consola despejada.
    - Mejora en el `hardware_mock.py` para incluir trazas de depuración al simular el procesamiento de comandos de la Raspberry Pi Pico.

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
