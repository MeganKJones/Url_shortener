from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, PlainTextResponse
from pydantic import BaseModel, HttpUrl
from typing import Dict
import secrets

app = FastAPI()

LOCAL_HOST = '0.0.0:8000'
fake_db: Dict[str, str] = {}


class URL(BaseModel):
    url: HttpUrl


def generate_shortened_url() -> str:
    while True:
        shortened_path = secrets.token_urlsafe(6)
        shortened_url = f'https://short.url/{shortened_path}'
        if shortened_url not in fake_db:
            return shortened_url


def get_key_from_value(value) -> str | None:
    for key, val in fake_db.items():
        if val == value:
            return key
    return None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/shorten/{url:path}")
async def url_shortener(url: str):
    shortened_url = generate_shortened_url()
    fake_db[shortened_url] = url
    print(fake_db)
    return URL(url=shortened_url)


@app.get('/redirect/{short_url:path}')
async def redirect_to_longer(short_url: str):
    path = fake_db[short_url]
    if short_url in fake_db:
        return RedirectResponse(f'/{path}')
    else:
        raise HTTPException(status_code=404, detail="URL not found")


@app.get('/{short_url:path}')
async def redirect(short_url: str):
    redirected_path = short_url.replace(f'{LOCAL_HOST}/', "")
    print(redirected_path)
    original_path = get_key_from_value(redirected_path)

    return {
        "message": "You have been redirected to long_url from short_url.",
        "long_url": f'{LOCAL_HOST}/{redirected_path}',
        "short_url": original_path,
    }
