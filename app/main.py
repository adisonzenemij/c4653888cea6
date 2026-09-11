from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.initialization import cors_origins, initialize_database

initialize_database()

# This order is used by Swagger UI instead of the order in which routers are registered.
openapi_tags = [
    {"name": "Autenticación"},
    {"name": "Alcances"},
    {"name": "Anónimos"},
    {"name": "Encuestas"},
    {"name": "Orígenes CORS"},
    {"name": "Preguntas"},
    {"name": "Respuestas"},
    {"name": "Tipos"},
    {"name": "Usuarios"},
    {"name": "Valores"},
    {"name": "JWT Permisos"}, {"name": "Entidades Módulos"}, {"name": "Entidades Recursos"},
    {"name": "Roles Datos"}, {"name": "Roles Accesos"}, {"name": "Roles Permisos"},
]

app = FastAPI(title="CUN Business API", version="1.0.0", openapi_tags=openapi_tags)
# The origin allow-list is read from sd_a1bb_a6baddf4c35a at application startup.
app.add_middleware(CORSMiddleware, allow_origins=cors_origins(), allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

from app.controllers.sd_1a9ea48c_ctrl import router as cors_router
from app.controllers.sd_3a731d00_ctrl import router as method_router
from app.controllers.pm_0dfa99e2_ctrl import router as service_router
from app.controllers.pm_5d0ddf5b_ctrl import router as resource_router
from app.controllers.pm_7ea81ec6_ctrl import router as society_router
from app.controllers.tg_5c72c20c_ctrl import router as user_router
from app.controllers.pm_1a4a8cd7_ctrl import router as anonymous_router
from app.controllers.pm_8e417bb2_ctrl import router as scope_router
from app.controllers.pm_0d3dc00e_ctrl import router as type_router
from app.controllers.pm_4d802b91_ctrl import public_router as public_survey_router, router as survey_router
from app.controllers.public_participation_ctrl import router as public_participation_router
from app.controllers.pm_0acc84ae_ctrl import router as question_router
from app.controllers.pm_9a582ff6_ctrl import router as value_router
from app.controllers.pm_3d86d159_ctrl import router as answer_router
from app.controllers.metadata_ctrl import jwt_router, module_router, resource_router as metadata_resource_router, role_data_router, role_access_router, role_permit_router

for router in (
    cors_router, method_router, service_router, resource_router, society_router, user_router,
    anonymous_router, scope_router, type_router, survey_router, question_router,
    value_router, answer_router,
    jwt_router, module_router, metadata_resource_router, role_data_router, role_access_router, role_permit_router,
):
    app.include_router(router, prefix="/api")
app.include_router(public_survey_router, prefix="/api")
app.include_router(public_participation_router, prefix="/api")


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
