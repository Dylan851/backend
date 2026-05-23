from fastapi import APIRouter

from app.controllers import animal_controller

router = APIRouter(prefix="/animals", tags=["animals"])

router.get("/nearby")(animal_controller.nearby_animals)
router.post("/capture")(animal_controller.capture_animal)
router.get("")(animal_controller.list_animals)
router.get("/{animal_id}")(animal_controller.get_animal_detail)
router.post("/{animal_id}/capture")(animal_controller.capture_animal_by_path)
