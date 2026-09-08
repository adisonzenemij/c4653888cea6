<h1 align="center">🔥 Proyecto Backend 🧑‍💻</h1>

## Introducción

## Requisitos

- Python 3.13.x

## Instalación

```yml
Clonar repositorio: git clone <project>
```

## Configuración

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

La API usa SQLite por defecto (`business.db`). Para MySQL, copie `.env.example` a `.env` y configure `DB_HOST`, `DB_USER`, `DB_PASS`, `DB_PORT` y `DB_NAME`; estas variables tienen prioridad sobre `DATABASE_URL`.
Al iniciar, crea las tablas y carga los valores iniciales. Los CORS se leen de `sd_a1bb_a6baddf4c35a` durante el arranque.

AutenticaciÃ³n: `POST /api/v1/auth/login` con `{"fd_login":"root","fd_passd":"<contraseÃ±a>"}` devuelve un Bearer JWT. Todas las rutas de recursos exigen ese token.

Cada recurso habilitado ofrece `GET /`, `GET /page?offset=0&limit=25`, `POST /`, `PUT /{id_universal}` y `DELETE /{id_universal}`, conforme a la matriz entregada.

`pm_answer` se publica como `/api/v1/answers` y, segÃºn su matriz, expone creaciÃ³n, actualizaciÃ³n y eliminaciÃ³n.

## Ejecuciones

```yml
Run: .venv\Scripts\python -m uvicorn main:app --reload
Run: .venv\Scripts\python -m uvicorn main:app --port 0000 --reload
Run: .venv\Scripts\python -m uvicorn main:app --host 0.0.0.0 --port 0000 --reload
```

## Comandos de Windows

```yml
# Permitir scripts solo en la sesión actual
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

## Documentación

```yml
ReDoc: http://0.0.0.0:0000/redoc
Swagger UI: http://0.0.0.0:0000/docs
Arquitectura: docs/arquitectura.md
```

## Docker

```yml
Comando: docker compose -f compose.yaml up -d --build
```

## Páginas oficiales

<div align="center">
    <a href="https://www.adisonjimenez.net" target="_blank">
        <span>Web principal</span>
    </a>
</div>
