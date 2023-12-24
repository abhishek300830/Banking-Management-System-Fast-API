from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import customer, auth_operations, account
from src.helpers.logger_config import initialize_main_logger

logger = initialize_main_logger(__name__)
logger.info("Application started")

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost:4200/login",
    "http://localhost:4200/account/balance",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=origins,
    allow_credentials=True,
    expose_headers=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account.router)
app.include_router(auth_operations.router)
app.include_router(customer.router)
