from fastapi import APIRouter

from app.controllers import animal_controller

router = APIRouter(prefix="/animals", tags=["animals"])

router.get("/nearby")(animal_controller.nearby_animals)
router.post("/capture")(animal_controller.capture_animal)
