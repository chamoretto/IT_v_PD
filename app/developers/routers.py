from fastapi import APIRouter, Security, Request
from pony.orm import db_session
from fastapi.responses import FileResponse, RedirectResponse

from app.developers.security import get_current_dev
from app.utils.jinja2_utils import developer_templates, db_templates
from app.utils.html_utils import Alert
from app.pydantic_models.gen import output_ent as out_pd
from app.pydantic_models.standart_methhods_redefinition import AccessType, AccessMode
from app.db import models as m

dev = APIRouter(
    prefix="/dev",
    tags=["developer"],
    dependencies=[
        # Depends(open_db_session),
        Security(get_current_dev, scopes=[str(AccessType.DEVELOPER)])
    ],  #
    responses={404: {"description": "Not found"}},
)


@dev.get("/me")
@db_session
def personal_page(request: Request, me=Security(get_current_dev, scopes=[str(AccessType.DEVELOPER)])):
    me.scopes += [str(AccessType.SELF)]
    return developer_templates.TemplateResponse("personal_page.html", {
        "request": request,
        "alert": Alert("Вы вошли в личный кабинет!", Alert.SUCCESS),
        "personal_data": db_templates.get_cooked_template(
            "Developer_form.html", {"request": request,
                                    "developer": out_pd.Developer(**dict(me)),
                                    "access": me.scopes,
                                    'access_mode': AccessMode.LOOK,
                                    "db_mode": False}),
    })


@dev.get("/logs", response_class=FileResponse)
async def get_logs():
    return FileResponse("../logs/рандомные_логи.log")


@dev.get("/stop_server")
def get_logs():
    from os import execl
    from sys import argv, executable
    # _io.TextIOWrapper

    # stdout
    changed_args = argv
    python = executable
    print('Restarting program. Arguments {}'.format(changed_args), python)
    yield {"answer": "Сервер будет остановлен"}
    execl(python, python, *changed_args)


@dev.get("/test_redirect", response_class=RedirectResponse)
def test_redirect(request: Request):
    return RedirectResponse("https://typer.tiangolo.com")