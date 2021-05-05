from app.utils.jinja2_utils import MyJinja2Templates

from app.db.db_utils import connect_with_db


connect_with_db()

login_templates = MyJinja2Templates(directory="content/templates/login")
error_templates = MyJinja2Templates(directory="content/templates/errors")