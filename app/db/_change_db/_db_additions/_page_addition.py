from app.db._change_db._db_additions._base_additions import _raw_m


def important_field_for_print(cls):
    return ["id", "title", "page_url", "is_header", "visible"]


_raw_m.db.entities["Page"].only_classmetod(important_field_for_print)


def get_header_menu_html_code(self):
    if not self.is_header:
        return ""
    if self.child_pages.is_empty():  # если дочерних страниц нет
        return (
            f'<li class="f-header__item margin-x-sm">'
            f'<a class="f-header__link" href="{self.page_url}">{self.title}'
            f"</a>"
            f"</li>"
        )
    options = "\n".join(
        [
            f'<li><a class="f-header__dropdown-link"' f' href="{page.page_url}">{page.title}</a>' f"</li>"
            for page in self.child_pages.select(lambda i: i.visible)[:]
        ]
    )

    return f"""<li class="f-header__item margin-x-sm">
    <a class="f-header__link">{self.title}
    <i class="icon text-center fa fa-caret-down"></i></a>
    <ul class="f-header__dropdown">{options}</ul></li>"""


_raw_m.db.entities["Page"].only_func(get_header_menu_html_code)
