from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.initialization import cors_origins, initialize_database

initialize_database()
app = FastAPI(title="CUN Business API", version="1.0.0")
# The origin allow-list is read from sd_a1bb_a6baddf4c35a at application startup.
app.add_middleware(CORSMiddleware, allow_origins=cors_origins(), allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

from app.controllers.sd_1a9ea48c_ctrl import router as cors_router
from app.controllers.tg_5c72c20c_ctrl import router as user_router
from app.controllers.pm_1a4a8cd7_ctrl import router as anonymous_router
from app.controllers.pm_8e417bb2_ctrl import router as scope_router
from app.controllers.pm_0d3dc00e_ctrl import router as type_router
from app.controllers.pm_4d802b91_ctrl import router as survey_router
from app.controllers.pm_0acc84ae_ctrl import router as question_router
from app.controllers.pm_9a582ff6_ctrl import router as value_router
from app.controllers.pm_3d86d159_ctrl import router as answer_router

for router in (cors_router, user_router, anonymous_router, scope_router, type_router, survey_router, question_router, value_router, answer_router):
    app.include_router(router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
