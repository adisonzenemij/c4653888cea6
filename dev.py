"""Development server with automatic reload for source code and .env changes."""

import os

from dotenv import dotenv_values
import uvicorn


if __name__ == "__main__":
    environment = dotenv_values(".env")
    host = str(os.getenv("DEV_HOST") or environment.get("DEV_HOST") or "0.0.0.0")
    try:
        port = int(os.getenv("DEV_PORT") or environment.get("DEV_PORT") or 4159)
    except ValueError as error:
        raise SystemExit("DEV_PORT debe ser un número entero válido.") from error

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        reload_dirs=["."],
        reload_includes=[".env"],
    )
