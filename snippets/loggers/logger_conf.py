import logging

# *********************************************
# Estas configuraciones son para poder silencias los logs
# de la libreria telegram-bot y solo ver los de la aplicacion
# *********************************************

# Configuración del logger para tu aplicación
logging.basicConfig(level=logging.INFO)
# Tu aplicación mostrará mensajes a partir del nivel INFO

# Silenciar los logs de la librería de telegram-bot
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

# *********************************************
# Configuracion de logger especifica:
# Si se dese acontrol mas detallado sobre los logs
# *********************************************

# Crear un logger customizado para tu aplicación
my_app_logger = logging.getLogger("mi_aplicacion")
my_app_logger.setLevel(logging.DEBUG)

# Crear y configurar el handler de consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Agregar el handler al logger de tu aplicación
my_app_logger.addHandler(console_handler)

# Ahora, puedes usar `my_app_logger` en tu código
my_app_logger.info("Este es un mensaje de tu aplicación.")

# Los mensajes de la librería de Telegram no se verán,
# a menos que configures un handler para el logger raíz.


# *********************************************
# Inicializacion detallada de logger
# *********************************************

def logger_config_v2():
    """Set up a logger with file and console handlers."""

    # Crear un logger
    logger = logging.getLogger("mi_app_logger")
    logger.setLevel(logging.DEBUG)

    # Crear un handler de archivo
    file_handler = logging.FileHandler("mi_app.log")
    file_handler.setLevel(logging.DEBUG)

    # Crear un handler de consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Definir el formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Agregar los handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
