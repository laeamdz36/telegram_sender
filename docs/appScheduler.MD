En add_job(), cuando usas trigger='cron', puedes especificar los siguientes campos de tiempo:

- year: El año.
- month: El mes (1-12).
- day: El día del mes (1-31).
- week: La semana del año (1-53).
- day_of_week: El día de la semana (0-6 o mon, tue, etc.).
- hour: La hora (0-23).
- minute: El minuto (0-59).
- second: El segundo (0-59).

Puedes usar asteriscos (*) para indicar "cualquier valor" y rangos como hour='9-17' o listas como day_of_week='mon,wed,fri'. En tu caso, para un horario fijo diario, solo necesitas especificar la hora y el minuto.