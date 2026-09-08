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
