def init_template_filters(app):
    @app.template_filter("get_initials")
    def get_initials(name):
        return "".join([part[0].upper() for part in name.strip().split(" ")[0:2]])