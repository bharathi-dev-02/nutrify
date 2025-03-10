class DatabaseRouter:
    def db_for_read(self, model, **hints):
        """Point Diabetes Analysis models to 'da_db'"""
        if model._meta.app_label == 'analysis':
            return 'da_db'
        return 'default'

    def db_for_write(self, model, **hints):
        """Point Diabetes Analysis models to 'da_db'"""
        if model._meta.app_label == 'analysis':
            return 'da_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation if both models are in the same database."""
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that apps only migrate in the correct database."""
        if app_label == 'analysis':
            return db == 'da_db'
        return db == 'default'
