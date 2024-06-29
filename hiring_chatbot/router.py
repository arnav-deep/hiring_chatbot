class Router:
    def db_for_read(self, model, **hints):
        return "default"

    def db_for_write(self, model, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return False
