from fastapi import FastAPI
from ticket import router as ticket_router
from interaction import router as interaction_router

from customer import router as customer_router


app = FastAPI(
    title="EnterpriseBrain 360",
    description="AI-Powered Enterprise Knowledge & Customer Intelligence Platform",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to EnterpriseBrain 360",
        "status": "Backend is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "EnterpriseBrain 360",
        "version": "1.0.0"
    }


# Register Customer APIs
app.include_router(customer_router)
app.include_router(ticket_router)
app.include_router(interaction_router)