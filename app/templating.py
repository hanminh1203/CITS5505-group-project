import re


def init_template_filters(app):
    @app.template_filter("get_initials")
    def get_initials(name):
        return "".join(
            [part[0].upper() for part in name.strip().split(" ")[0:2]]
        )

    @app.template_filter("format_request_status")
    def format_request_status(status):
        return re.sub(r'[ _]', '-', status.name).lower()
