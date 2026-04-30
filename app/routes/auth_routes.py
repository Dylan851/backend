from fastapi import APIRouter

from app.controllers import auth_controller

router = APIRouter(prefix="/auth", tags=["auth"])

router.post("/register")(auth_controller.register)
router.post("/login")(auth_controller.login)
router.post("/google")(auth_controller.google_auth)
