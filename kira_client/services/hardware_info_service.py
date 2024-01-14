class HardwareInfoService:
    cpu_temp = None

    def __init__(self, enabled: bool):
        if not enabled:
            return

        from gpiozero import CPUTemperature

        self.cpu_temp = CPUTemperature()

    def get_cpu_temperature(self) -> float:
        if not self.cpu_temp:
            return 0.0

        return self.cpu_temp.temperature
