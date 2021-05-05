from app.pydantic_models.standart_methhods_redefinition import BaseModel


class Alert:
    # PRIMARY = "primary"
    # SECONDARY = "secondary"
    SUCCESS = "success"
    # DANGER = "danger"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

    # LIGHT = "light"
    # DARK = "dark"

    def __init__(self, content: str, alert_type=SUCCESS):
        self.content = content
        self.alert_type = alert_type

    @property
    def conv(self):
        return {
            "content": self.content,
            "type": self.alert_type
        }

    def __dir__(self):
        return self.conv

    def __str__(self):
        return 'Alert(%s): "%s"' % (self.alert_type.capitalize(), self.content)

    def __repr__(self):
        return "<Alert(%s) %.10s>" % (self.alert_type.capitalize(), self.content)


class SitePageMenu(BaseModel):
    name: str
    href: str = "*"