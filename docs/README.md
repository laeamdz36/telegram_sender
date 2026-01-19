### Web server for notifications

Gunicorn as the process manager, WSGI, robust handling of the process worker as uvicorn

Uvicorn as the ASGI, Asynchronous Server Gateway Interfacem, lightweight and fast, designed to execute aplications asynchronous as FastAPI, based in async and await

```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Phrase of the day

{"phrase":"La dificultad es una excusa que la historia nunca acepta.","author":"Edward R. Murrow"}

https://proverbia.net/frase-del-dia

https://frasedeldia.azurewebsites.net/api/phrase

### Workaround Fastapi, enpoint post to DB

¿Por qué esto arregla tu error?
Validación Aislada: Cuando FastAPI recibe el JSON, usa PersonCreate. Al ver birth_date: date, transforma el string "1990-07-24" en un objeto datetime.date(1990, 7, 24).

Transferencia Segura: Luego, Person.model_validate(person_data) toma esos datos (que ya son fechas seguras) y crea el objeto de base de datos.

SQLAlchemy Feliz: Cuando haces session.add(person_db), la propiedad birth_date ya es un objeto fecha de Python, y SQLite no se queja.