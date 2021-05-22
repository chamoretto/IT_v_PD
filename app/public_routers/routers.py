from fastapi import Request
from fastapi.responses import HTMLResponse
from pony.orm import db_session

from fastapi import status, APIRouter

from app.dependencies import *
from app.db import models as m
from app.pydantic_models.gen import db_models_for_create as pd, output_ent as out_pd
from app.pydantic_models import simple_entities as easy_ent_pd
from app.utils.jinja2_utils import public_templates
from app.utils.exceptions import ChildHTTPException as HTTPException


public_router = APIRouter()
error_404_Page = dict(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Страниа не найдена",
    )

@public_router.get('/')
@db_session
def main_page(request: Request):
    return public_templates.TemplateResponse("main.html", {
        "request": request,
        "partner": [easy_ent_pd.Partner(id=key, **val) for key, val in dict(m.SimpleEntity['partner'].data).items()],
        "socials": [easy_ent_pd.Socials(id=key, **val) for key, val in dict(m.SimpleEntity['socials'].data).items()],
        "graduates": [out_pd.User.from_pony_orm(i) for i in m.User.select(lambda i: i.visible_about_program_field)[:]],
        # "events": True
    })


# @public_router.get('/content/public/{file_path:path}')
# async def get_public_files(file_path: str):
#     file_path = os_join("content", "public", file_path)
#     return FileResponse(file_path)


@public_router.post('/test_auto_pd_human')
async def test_pd(pd_model: pd.Human):
    return pd_model


@public_router.get('/test_jinja', response_class=HTMLResponse)
async def start_public_router(request: Request):
    return login_templates.TemplateResponse(
        "login.html",
        {"request": request, "who": "Редактораdffffffffffff", "auth_url": '/' + "token_path"})


@public_router.get("/videostudy")
@db_session
def get_public_pages(request: Request):
    print('rfgsdg')
    if (ent := m.Page.get(page_url="/videostudy")) or (ent := m.Page.get(page_url="videostudy")):
        return public_templates.TemplateResponse(ent.page_path, {
            "request": request,
            "directions": [out_pd.Direction.from_pony_orm(i) for i in m.Direction.select()[:]]})
    raise HTTPException(request=request, **error_404_Page)


@public_router.get("/videostudy/{direction}")
@db_session
def get_public_pages(request: Request, direction: str):
    print("------------------------------------")
    if ent := m.Direction.get(name=direction):
        return public_templates.TemplateResponse("videostudy/videostudy_direction.html", {
            "request": request,
            "direction": out_pd.Direction.from_pony_orm(ent)})

    raise HTTPException(request=request, **error_404_Page)



@public_router.get("/events/{event}")
@db_session
def get_public_pages(request: Request, event: str):
    print("------------------------------------")
    if (ent := m.Page.get(page_url="/events/" + event)) or (ent := m.Page.get(page_url="events/" + event)):
        return public_templates.TemplateResponse(ent.page_path, {
            "request": request})

    raise HTTPException(request=request, **error_404_Page)


@public_router.get("/news")
@db_session
def get_public_pages(request: Request):
    print('rfgsdg')
    if (ent := m.Page.get(page_url="/news")) or (ent := m.Page.get(page_url="news")):
        return public_templates.TemplateResponse(ent.page_path, {
            "request": request,
            "news": [out_pd.News.from_pony_orm(i) for i in m.News.select()[:]]})
    raise HTTPException(request=request, **error_404_Page)


@public_router.get("/news/{post}")
@db_session
def get_public_pages(request: Request, post: str):
    print("------------------------------------")
    if (ent := m.News.get(page_url="/news/" + post)) or (ent := m.News.get(page_url="news/" + post)):
        return public_templates.TemplateResponse("news/one_post.html", {
            "request": request,
            "socials": [easy_ent_pd.Socials(id=key, **val) for key, val in dict(m.SimpleEntity['socials'].data).items()],
            "post": out_pd.News.from_pony_orm(ent)
        })

    raise HTTPException(request=request, **error_404_Page)


@public_router.get("/about_program")
@db_session
def get_public_pages(request: Request):
    if (ent := m.Page.get(page_url="/about_program")) or (ent := m.Page.get(page_url="about_program")):
        return public_templates.TemplateResponse(ent.page_path, {
            "request": request})
    raise HTTPException(request=request, **error_404_Page)


# @public_router.get("/competition")
# @db_session
# def get_public_pages(request: Request):
#     if (ent := m.Page.get(page_url="/competition")) or (ent := m.Page.get(page_url="competition")):
#         return public_templates.TemplateResponse(ent.page_path, {
#             "request": request,
#             "directions": [out_pd.Direction.from_pony_orm(i) for i in m.Direction.select()[:]]})
#     raise HTTPException(request=request, **error_404_Page)
#
#
# @public_router.get("/competition/{direction}")
# @db_session
# def get_public_pages(request: Request, direction: str):
#     if ent := m.Direction.get(name=direction):
#         return public_templates.TemplateResponse("competition/direction.html", {
#             "request": request,
#             "direction": out_pd.Direction.from_pony_orm(ent)})
#
#     raise HTTPException(request=request, **error_404_Page)

# @public_router.get("/{file_path:path}")
# @db_session
# def get_public_pages(file_path: str, request: Request):
#     print('=-098765456789', file_path)
#     file_path = file_path.removeprefix("/")
#     ent = None
#     if m.Page.exists(page_url=file_path):
#         print('456')
#         ent = m.Page.get(page_url=file_path)
#
#     elif m.Page.exists(page_url="/" + file_path):
#         print('4erter')
#         ent = m.Page.get(page_url="/" + file_path)
#     print(ent)
#     if ent:
#         return public_templates.TemplateResponse(ent.page_path, {"request": request})
#     raise HTTPException(request=request, **error_404_Page)