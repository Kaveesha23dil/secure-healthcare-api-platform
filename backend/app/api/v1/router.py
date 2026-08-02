from fastapi import APIRouter

from app.api.v1 import admin, appointments, availability, doctors, patients

router = APIRouter(prefix="/api/v1")
router.include_router(doctors.router)
router.include_router(availability.router)
router.include_router(appointments.router)
router.include_router(patients.router)
router.include_router(admin.router)
