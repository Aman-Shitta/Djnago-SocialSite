from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'profiles'

    def ready(self):
        print("************************************************************************************SIGNALS RUN************************************************************************************")
        import profiles.signals   # initialize signals