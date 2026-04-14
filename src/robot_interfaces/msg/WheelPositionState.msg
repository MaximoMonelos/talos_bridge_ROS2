std_msgs/Header header
string  wheel_id

float32 position_deg        # grados acumulados desde arranque
float32 setpoint_deg        # grados objetivo actual
float32 error_deg           # setpoint - position actual
float32 pid_output          # salida PID normalizada [-1.0, 1.0]

bool    is_online