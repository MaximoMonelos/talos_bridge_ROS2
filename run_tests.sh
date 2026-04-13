#!/bin/bash

# Script para correr tests de ROS 2 en el workspace de Talos SN de forma verbosa.

# 1. Compilar el workspace (asegura que los tests estén actualizados)
echo "Compilando el workspace..."
colcon build --symlink-install

# Comprobar si la compilación fue exitosa
if [ $? -ne 0 ]; then
    echo "ERROR: La compilación falló. Abortando tests."
    exit 1
fi

# 2. Cargar el entorno
if [ -f "install/setup.bash" ]; then
    source install/setup.bash
else
    echo "ERROR: Archivo install/setup.bash no encontrado. ¿Compilaste el workspace?"
    exit 1
fi

# 3. Ejecutar los tests con salida verbosa directa a consola
echo "Ejecutando tests de ROS 2..."
# --event-handlers console_direct+: muestra stdout/stderr de los tests en vivo.
# --return-code-on-test-failure: asegura que colcon devuelva un error si algún test falla.
colcon test --event-handlers console_direct+ --return-code-on-test-failure

# Guardar el código de salida de colcon test
TEST_EXIT_CODE=$?

# 4. Mostrar resumen detallado de resultados
echo "--------------------------------------------------"
echo "Resumen detallado de los resultados:"
colcon test-result --all --verbose

# Guardar código de salida final
FINAL_EXIT_CODE=$TEST_EXIT_CODE

# Mantener la terminal abierta al final
echo ""
echo "Presiona Enter para cerrar esta ventana..."
read -r

# Retornar o salir dependiendo de cómo se ejecutó el script
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    return $FINAL_EXIT_CODE
else
    exit $FINAL_EXIT_CODE
fi
