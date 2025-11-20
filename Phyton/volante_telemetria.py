# Sistema de Telemetría para Volante de Carreras Eléctrico
# MicroPython para Raspberry Pi Pico W

from machine import ADC, Pin, I2C
from time import sleep, time
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import network
import socket
import uos
import json

class Configuracion:
    """Clase para manejar la configuración del sistema"""
    def __init__(self):
        # Pines
        self.__PIN_SCT013 = 26  # ADC0
        self.__PIN_BOTON = 14
        self.__PIN_LCD_SDA = 0
        self.__PIN_LCD_SCL = 1
        
        # Configuración LCD
        self.__LCD_I2C_ADDR = 0x27
        self.__LCD_FILAS = 2
        self.__LCD_COLUMNAS = 16
        
        # Configuración batería
        self.__VOLTAJE_NOMINAL = 48.0  # 4 baterías de 12V en serie
        self.__CAPACIDAD_AH = 17.0 #Maxima corriente que proveen
        self.__CAPACIDAD_WH = self.__VOLTAJE_NOMINAL * self.__CAPACIDAD_AH
        
        # Configuración carrera
        self.__TIEMPO_VUELTA_MIN = 2.0  # minutos (este valor depende de la velocidad de la carrera)
        self.__VUELTAS_PLANEADAS = 10 # este valor depende de la distancia de la carrera
        
        # Umbrales de advertencia
        self.__BATERIA_BAJA = 10  # porcentaje de bateria restante hasta que la controladora entra en modo de bajo consumo
        self.__POTENCIA_ALTA = 2000  # watts
        self.__POTENCIA_BAJA = 100  # watts
        
        # Wi-Fi
        self.__WIFI_SSID = 'ECODESAFIO'
        self.__WIFI_PASSWORD = 'sarra123'

    # Getters para pines
    @property
    def PIN_SCT013(self):
        return self.__PIN_SCT013

    @property
    def PIN_BOTON(self):
        return self.__PIN_BOTON

    @property
    def PIN_LCD_SDA(self):
        return self.__PIN_LCD_SDA

    @property
    def PIN_LCD_SCL(self):
        return self.__PIN_LCD_SCL

    # Getters para configuración LCD
    @property
    def LCD_I2C_ADDR(self):
        return self.__LCD_I2C_ADDR

    @property
    def LCD_FILAS(self):
        return self.__LCD_FILAS

    @property
    def LCD_COLUMNAS(self):
        return self.__LCD_COLUMNAS

    # Getters para configuración batería
    @property
    def VOLTAJE_NOMINAL(self):
        return self.__VOLTAJE_NOMINAL

    @property
    def CAPACIDAD_AH(self):
        return self.__CAPACIDAD_AH

    @property
    def CAPACIDAD_WH(self):
        return self.__CAPACIDAD_WH

    # Getters para configuración carrera
    @property
    def TIEMPO_VUELTA_MIN(self):
        return self.__TIEMPO_VUELTA_MIN

    @property
    def VUELTAS_PLANEADAS(self):
        return self.__VUELTAS_PLANEADAS

    # Getters para umbrales de advertencia
    @property
    def BATERIA_BAJA(self):
        return self.__BATERIA_BAJA

    @property
    def POTENCIA_ALTA(self):
        return self.__POTENCIA_ALTA

    @property
    def POTENCIA_BAJA(self):
        return self.__POTENCIA_BAJA

    # Getters para Wi-Fi
    @property
    def WIFI_SSID(self):
        return self.__WIFI_SSID

    @property
    def WIFI_PASSWORD(self):
        return self.__WIFI_PASSWORD

class SensorCorriente:
    """Clase para manejar el sensor SCT-013"""
    def __init__(self, pin_adc):
        self.sensor = ADC(Pin(pin_adc))
        self.factor_calibracion = 0.066  # Ajustar según calibración
        
    def leer(self):
        """Lee la corriente en amperios"""
        muestras = [self.sensor.read_u16() for _ in range(100)]
        media = sum(muestras) / len(muestras)
        voltaje = media * 3.3 / 65535
        corriente = (voltaje - 1.65) / self.factor_calibracion
        return abs(corriente)

class PantallaLCD:
    """Clase para manejar la pantalla LCD I2C"""
    def __init__(self, sda_pin, scl_pin, addr, filas, columnas):
        self.i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=400000)
        self.lcd = I2cLcd(self.i2c, addr, filas, columnas)
        
    def mostrar_datos(self, datos):
        """Muestra los datos en la pantalla LCD"""
        self.lcd.clear()
        # Primera línea: Corriente y Voltaje
        self.lcd.putstr("I:{:.1f}A V:{:.1f}V".format(
            datos['corriente'], datos['voltaje']))
        
        # Segunda línea: Potencia y Batería
        self.lcd.move_to(0, 1)
        self.lcd.putstr("P:{:.0f}W B:{:.0f}%".format(
            datos['potencia'], datos['bateria']))
        sleep(0.5)
        
        # Tercera línea: Tiempo y Vueltas
        self.lcd.clear()
        minutos = int(datos['tiempo_restante'] / 60)
        segundos = int(datos['tiempo_restante'] % 60)
        self.lcd.putstr("T:{:02d}:{:02d} V:{}".format(
            minutos, segundos, int(datos['vueltas_restantes'])))
        
        # Cuarta línea: Advertencias
        self.lcd.move_to(0, 1)
        if datos['bateria'] < 10:
            self.lcd.putstr("ADVERTENCIA: <10%")
        elif datos['potencia'] > 2000:
            self.lcd.putstr("CONSUMO ALTO!")
        elif datos['potencia'] < 100:
            self.lcd.putstr("CONSUMO BAJO!")
        else:
            self.lcd.putstr("CONSUMO NORMAL")
        sleep(0.5)

class Bateria:
    """Clase para manejar la estimación de batería"""
    def __init__(self, config):
        self.config = config
        self.curva_descarga = [
            (52.0, 100), (51.2, 90), (50.2, 80),
            (49.6, 70), (48.4, 60), (47.3, 50),     #A futuro se piensa ajustar estos valores a los obtenidos con los obtenidos del analisis de la curva 
            (46.4, 40), (45.3, 30), (44.4, 20),
            (43.2, 10), (42.0, 0)
        ]
        self.acumulado_wh = 0.0
        
    def estimar_porcentaje(self, voltaje):
        """Estima el porcentaje de batería basado en el voltaje"""
        for i in range(len(self.curva_descarga) - 1):
            v1, p1 = self.curva_descarga[i]
            v2, p2 = self.curva_descarga[i + 1]
            if v1 >= voltaje >= v2:
                return p1 + (p2 - p1) * (voltage - v1) / (v2 - v1)
        return 0
        
    def actualizar(self, potencia, delta_t):
        """Actualiza el estado de la batería"""
        self.acumulado_wh += potencia * (delta_t / 3600.0)
        voltaje = self.config.VOLTAJE_NOMINAL - (self.acumulado_wh / self.config.CAPACIDAD_WH) * 16.0
        porcentaje = self.estimar_porcentaje(voltaje)
        return voltaje, porcentaje

class ServidorWeb:
    """Clase para manejar el servidor web"""
    def __init__(self, config):
        self.config = config
        self.html_template = self.cargar_template()
        
    def cargar_template(self):
        """Carga la plantilla HTML desde el archivo"""
        try:
            with open('templates/index.html', 'r') as f:
                return f.read()
        except:
            # Si no se puede cargar el archivo, usar una versión básica
            return """
            <!DOCTYPE html>
            <html>
              <head>
                <title>EcoDesafio</title>
                <meta http-equiv="refresh" content="2">
              </head>
              <body>
                <h2>Telemetría del vehículo</h2>
                <p>Corriente: {corriente:.1f} A</p>
                <p>Voltaje: {voltaje:.1f} V</p>
                <p>Potencia: {potencia:.0f} W</p>
                <p>Batería: {bateria:.0f}%</p>
                <p>Vueltas restantes: {vueltas:.0f}</p>
                <p>Tiempo restante: {tiempo} min</p>
                <p class="{clase}">{mensaje}</p>
              </body>
            </html>
            """
        
    def iniciar(self, ip, datos_callback):
        """Inicia el servidor web"""
        addr = socket.getaddrinfo(ip, 80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        
        while True:
            cl, addr = s.accept()
            cl_file = cl.makefile('rwb', 0)
            while True:
                line = cl_file.readline()
                if not line or line == b'\r\n':
                    break
                    
            datos = datos_callback()
            respuesta = self.html_template.format(**datos)
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(respuesta)
            cl.close()

class RegistradorDatos:
    """Clase para manejar el registro de datos"""
    def __init__(self):
        self.archivo = None
        
    def iniciar_registro(self):
        """Inicia el registro de datos"""
        self.archivo = open("telemetria.csv", "w")
        self.archivo.write("Tiempo,Corriente,Voltaje,Potencia,Wh,Porcentaje,Vueltas\n")
        
    def registrar(self, datos):
        """Registra una línea de datos"""
        if self.archivo:
            self.archivo.write("{},{:.2f},{:.2f},{:.2f},{:.2f},{:.1f},{:.1f}\n".format(
                datos['tiempo'], datos['corriente'], datos['voltaje'],
                datos['potencia'], datos['energia_acumulada'],
                datos['bateria'], datos['vueltas_restantes']))
            self.archivo.flush()
            
    def cerrar(self):
        """Cierra el archivo de registro"""
        if self.archivo:
            self.archivo.close()
            self.archivo = None

class SistemaTelemetria:
    """Clase principal del sistema de telemetría"""
    def __init__(self):
        self.config = Configuracion()
        self.sensor = SensorCorriente(self.config.PIN_SCT013)
        self.pantalla = PantallaLCD(
            self.config.PIN_LCD_SDA,
            self.config.PIN_LCD_SCL,
            self.config.LCD_I2C_ADDR,
            self.config.LCD_FILAS,
            self.config.LCD_COLUMNAS
        )
        self.bateria = Bateria(self.config)
        self.registrador = RegistradorDatos()
        self.boton = Pin(self.config.PIN_BOTON, Pin.IN, Pin.PULL_UP)
        self.prueba_activa = False
        self.ultimo_tiempo = time()
        self.intervalo_medicion = 2  # Intervalo de medición en segundos
        
    def conectar_wifi(self):
        """Conecta a la red Wi-Fi"""
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.config.WIFI_SSID, self.config.WIFI_PASSWORD)
        while not wlan.isconnected():
            sleep(0.5)
        print("Conectado a Wi-Fi")
        print(wlan.ifconfig())
        return wlan.ifconfig()[0]
        
    def obtener_datos_web(self):
        """Obtiene los datos para la página web"""
        datos = self.obtener_datos_actuales()
        clase = "normal"
        mensaje = "Estado normal"
        
        if datos['bateria'] < self.config.BATERIA_BAJA:
            clase = "warning"
            mensaje = "ADVERTENCIA: Batería baja"
        elif datos['potencia'] > self.config.POTENCIA_ALTA:
            clase = "warning"
            mensaje = "ADVERTENCIA: Consumo alto"
        elif datos['potencia'] < self.config.POTENCIA_BAJA:
            clase = "warning"
            mensaje = "ADVERTENCIA: Consumo bajo"
            
        return {
            "corriente": datos['corriente'],
            "voltaje": datos['voltaje'],
            "potencia": datos['potencia'],
            "bateria": datos['bateria'],
            "vueltas": datos['vueltas_restantes'],
            "tiempo": int(datos['tiempo_restante'] / 60),
            "clase": clase,
            "mensaje": mensaje
        }
        
    def obtener_datos_actuales(self):
        """Obtiene los datos actuales del sistema"""
        ahora = time()
        delta_t = ahora - self.ultimo_tiempo
        self.ultimo_tiempo = ahora
        
        # Lectura de sensores
        corriente = self.sensor.leer()
        
        # Primero obtenemos el voltaje actual
        voltaje = self.config.VOLTAJE_NOMINAL - (self.bateria.acumulado_wh / self.config.CAPACIDAD_WH) * 16.0
        
        # Calculamos la potencia instantánea
        potencia = corriente * voltaje
        
        # Actualizamos el estado de la batería con la potencia calculada
        voltaje, porcentaje = self.bateria.actualizar(potencia, delta_t)
        
        # Cálculo de tiempo y vueltas restantes
        energia_rest = max(0, self.config.CAPACIDAD_WH - self.bateria.acumulado_wh)
        consumo_prom = self.bateria.acumulado_wh / (ahora / 60.0)
        tiempo_rest = energia_rest / consumo_prom if consumo_prom > 0 else 0
        vueltas_rest = tiempo_rest / self.config.TIEMPO_VUELTA_MIN
        
        return {
            'tiempo': ahora,
            'corriente': corriente,
            'voltaje': voltaje,
            'potencia': potencia,
            'energia_acumulada': self.bateria.acumulado_wh,
            'bateria': porcentaje,
            'vueltas_restantes': vueltas_rest,
            'tiempo_restante': tiempo_rest * 60
        }
        
    def esperar_proximo_intervalo(self):
        """Espera hasta el próximo intervalo de medición"""
        tiempo_actual = time()
        tiempo_espera = self.intervalo_medicion - (tiempo_actual - self.ultimo_tiempo)
        if tiempo_espera > 0:
            sleep(tiempo_espera)
        
    def iniciar(self):
        """Inicia el sistema de telemetría"""
        ip = self.conectar_wifi()
        servidor = ServidorWeb(self.config)
        
        # Iniciar servidor web en un hilo separado
        import _thread
        _thread.start_new_thread(servidor.iniciar, (ip, self.obtener_datos_web))
        
        self.pantalla.lcd.putstr("Esperando prueba")
        
        # Bucle principal
        while True:
            # Esperar hasta el próximo intervalo
            self.esperar_proximo_intervalo()
            
            # Obtener y mostrar datos
            datos = self.obtener_datos_actuales()
            self.pantalla.mostrar_datos(datos)
            
            # Registrar datos si la prueba está activa
            if self.prueba_activa:
                self.registrador.registrar(datos)
                
            # Control del botón (sin espera adicional para respuesta inmediata)
            if not self.boton.value():
                self.prueba_activa = not self.prueba_activa
                sleep(0.5)  # Debounce del botón
                if self.prueba_activa:
                    self.registrador.iniciar_registro()
                    self.bateria.acumulado_wh = 0
                    self.pantalla.lcd.clear()
                    self.pantalla.lcd.putstr("Inicio prueba")
                else:
                    self.pantalla.lcd.clear()
                    self.pantalla.lcd.putstr("Fin prueba")
                    self.registrador.cerrar()
                    
            sleep(1)

# Iniciar el sistema
if __name__ == "__main__":
    sistema = SistemaTelemetria()
    sistema.iniciar() 