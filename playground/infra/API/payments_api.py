from fastapi import APIRouter

payments_api = APIRouter()


@payments_api.get("/", status_code=201)
def calculate_payment():
    pass


@payments_api.post("/", status_code=200)
def add_payment():
    pass
