from fastapi.templating import Jinja2Templates

from app.db.db_utils import connect_with_db


connect_with_db()

login_templates = Jinja2Templates(directory="content/templates/login")