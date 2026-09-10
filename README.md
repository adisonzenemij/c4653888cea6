<h1 align="center">ðŸ”¥ Proyecto Backend ðŸ§‘â€ðŸ’»</h1>

## IntroducciÃ³n

## Requisitos

- Python 3.13.x

## InstalaciÃ³n

```yml
Clonar repositorio: git clone <project>
```

## ConfiguraciÃ³n

```yml
Entorno virtual: python -m venv .venv
Verificar entorno: python -m site
Generar archivo: pip freeze > requirements.txt
```

## Entorno virtual

```yml
Windows PS: .venv\Scripts\activate
Windows PS: .venv\Scripts\Activate.ps1
Windows CMD: .venv\Scripts\activate.bat
MacOS: source .venv/bin/activate
Linux: source .venv/bin/activate
```

## Dependencias

```yml
Requerimientos: .venv\Scripts\python -m pip install -r requirements.txt
```

## API

La API usa SQLite por defecto (`business.db`). Para MySQL, copie `.env.example` a `.env` y configure `DB_HOST`, `DB_USER`, `DB_PASS`, `DB_PORT` y `DB_NAME`; estas variables tienen prioridad sobre `DATABASE_URL`. Si la base no existe, la API la crea con `CHARACTER SET utf8mb4` y `COLLATE utf8mb4_general_ci` antes de crear las tablas.
Al iniciar, crea las tablas y carga los valores iniciales. Los CORS se leen de `sd_a1bb_a6baddf4c35a` durante el arranque.

AutenticaciÃƒÂ³n: `POST /api/auth/login` con `{"fd_login":"root","fd_passd":"<contraseÃƒÂ±a>"}` devuelve un Bearer JWT. Todas las rutas de recursos exigen ese token.

Cada recurso habilitado ofrece `GET /`, `GET /page?offset=0&limit=25`, `POST /`, `PUT /{id_universal}` y `DELETE /{id_universal}`, conforme a la matriz entregada.

`pm_answer` se publica como `/api/answers` y, segÃƒÂºn su matriz, expone creaciÃƒÂ³n, actualizaciÃƒÂ³n y eliminaciÃƒÂ³n.

## Ejecuciones

```yml
Run: .venv\Scripts\python -m uvicorn main:app --reload
Run: .venv\Scripts\python -m uvicorn main:app --port 0000 --reload
Run: .venv\Scripts\python -m uvicorn main:app --host 0.0.0.0 --port 0000 --reload
```

## Comandos de Windows

```yml
# Permitir scripts solo en la sesiÃ³n actual
PowerShell: Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

## Orden del ambiente

```yml
Entorno virtual: python -m venv .venv
Windows PS: .venv\Scripts\activate
Windows PS: .venv\Scripts\Activate.ps1
Windows CMD: .venv\Scripts\activate.bat
Verificar entorno: python -m site
Requerimientos: .venv\Scripts\python -m pip install -r requirements.txt
```

## DocumentaciÃ³n

```yml
ReDoc: http://0.0.0.0:0000/redoc
Swagger UI: http://0.0.0.0:0000/docs
Arquitectura: docs/arquitectura.md
```

## Docker

```yml
1. Copie `.env.example` como `.env` y configure las variables requeridas.
2. Comando: docker compose -f compose.yaml up -d --build
3. API: http://localhost:40159/docs
```

`compose.yaml` carga las variables desde `.env` con `env_file`; el archivo no se incluye en la imagen. Si MySQL se ejecuta en el equipo anfitrión, use `DB_HOST=host.docker.internal` en `.env` (en lugar de `127.0.0.1`). Para MySQL en otro contenedor conectado a la red `a690a01e6a6f`, use el nombre del servicio como host (`DB_HOST=mysql80`) y su puerto interno (`DB_PORT=3306`); el puerto publicado `43380` solo se usa desde el host. Puede cambiar el puerto publicado de la API con `API_PORT`, por ejemplo `API_PORT=8080`.

## PÃ¡ginas oficiales

<div align="center">
    <a href="https://www.adisonjimenez.net" target="_blank">
        <span>Web principal</span>
    </a>
</div>

