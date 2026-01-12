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