from fastapi import APIRouter

from app.controllers import auth_controller

router = APIRouter(prefix="/auth", tags=["auth"])

router.post("/register")(auth_controller.register)
router.post("/login")(auth_controller.login)
router.post("/google")(auth_controller.google_auth)
router.post("/supabase")(auth_controller.supabase_auth)
router.post("/methods")(auth_controller.auth_methods)
router.post("/password/recover")(auth_controller.recover_password)
