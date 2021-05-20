from fastapi import APIRouter, Depends, HTTPException, Security, Request
from pony.orm import db_session
from fastapi.responses import FileResponse, StreamingResponse

from app.dependencies import *
from app.pydantic_models.standart_methhods_redefinition import BaseModel
from app.developers.security import get_current_dev
from app.db.db_utils import open_db_session
from app.utils.pydantic_security import HumanInDB
from app.utils.jinja2_utils import developer_templates, db_templates
from app.utils.html_utils import Alert
from app.pydantic_models import output_ent as out_pd
from app.settings.config import HOME_DIR, join


dev = APIRouter(
    prefix="/dev",
    tags=["developer"],
    dependencies=[
        # Depends(open_db_session),
        Security(get_current_dev, scopes=["developer"])
    ],  #
    responses={404: {"description": "Not found"}},
)


@dev.get('/some')
async def start_dev():
    return {1: 1}


@dev.get("/me")
@db_session
def personal_page(request: Request, me=Security(get_current_dev, scopes=["developer"])):
    return developer_templates.TemplateResponse("personal_page.html", {
        "request": request,
        "alert": Alert("Вы вошли в личный кабинет!", Alert.SUCCESS),
        "personal_data": db_templates.get_cooked_template(
            "Developer_form.html", {"request": request,
                                    "developer": out_pd.Developer(**me.dict()),
                                    "action_url": f"/db/Developer/look/",
                                    "send_method": "POST",
                                    "disabled": True,
                                    'access_mode': 'look',
                                    "db_mode": False}),
    })


@dev.get("/logs", response_class=FileResponse)
async def get_logs():
    return FileResponse("../logs/рандомные_логи.log")


@dev.get("/stop_server")
def get_logs():
    from os import execl, fsync
    from sys import argv, executable, stdout, __stdout__
    import _io
    # _io.TextIOWrapper

    # stdout
    changed_args = argv
    python = executable
    print('Restarting program. Arguments {}'.format(changed_args), python)
    yield {"answer": "Сервер будет остановлен"}
    execl(python, python, *changed_args)