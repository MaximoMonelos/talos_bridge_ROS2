# Coding Standards - Talos Robotics

## General Rules
- Estándar de C++: C++17 (para compatibilidad con Jazzy).
- Estándar de Python: PEP8.
- Documentación: Todo debe estar listo para Obsidian (Markdown con Mermaid para diagramas).

## ROS 2 Jazzy Specifics
- Siempre usar `rclcpp` o `rclpy`.
- No usar llamadas síncronas en servicios (evitar deadlocks).
- Priorizar el uso de `Composition` y `LifeCycle Nodes` si es posible.
- Los tópicos deben seguir la nomenclatura: `/robot_name/sensor_type/data`.

## Embedded (micro-ROS)
- Optimizar el uso de memoria para el RP2350.
- Evitar asignación dinámica de memoria en el loop principal.
