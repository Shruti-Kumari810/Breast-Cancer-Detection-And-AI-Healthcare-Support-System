from fastapi import APIRouter

from app.api.v1.endpoints import analytics, appointments, auth, doctors, patients, predictions, resources

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(patients.router, prefix="/patients", tags=["Patients"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])
api_router.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
api_router.include_router(resources.router, prefix="/resources", tags=["Health Resources"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Dashboard Analytics"])

