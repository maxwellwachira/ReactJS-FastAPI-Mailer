from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.responses import JSONResponse
from starlette.requests import Request
from decouple import config
from app.models import EmailSchema
from pathlib import Path


conf = ConnectionConfig(
    MAIL_USERNAME = config("MAIL_USERNAME"),
    MAIL_PASSWORD = config("MAIL_PASSWORD"),
    MAIL_FROM = config("MAIL_FROM"),
    MAIL_PORT = config("MAIL_PORT"),
    MAIL_SERVER = config("MAIL_SERVER"),
    MAIL_TLS = config("MAIL_TLS"),
    MAIL_SSL = config("MAIL_SSL"),
    USE_CREDENTIALS = config("USE_CREDENTIALS"),
    VALIDATE_CERTS = config("VALIDATE_CERTS"),
    TEMPLATE_FOLDER = Path(__file__).parent / '../templates/email',
   
)


app = FastAPI(title='Sending Email using FastAPI and React')

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Redirect to API documentation
@app.get("/", tags=["Redirect to API Documentation"])
async def documentation_redirect ():
    return RedirectResponse('/docs')


#Send Email Asynchronously
@app.post("/send-email-async", tags=["Send Email Asynchronously"])
async def send_email_async(data: EmailSchema) -> JSONResponse:
    post_data = data.dict()
   
    message = MessageSchema (
        subject = post_data["subject"],
        recipients = [post_data["email"]],
        template_body=post_data["body"],
        subtype="html"
    )
    fm = FastMail(conf)

    try:
        await fm.send_message(message, template_name="email.html")
        return JSONResponse(status_code=200, content={"message": "success"})
    except Exception as e:
        return JSONResponse(status_code=503, content={"message": e})


