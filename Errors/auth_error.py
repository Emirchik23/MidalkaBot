class AuthError(Exception):
    def __init__(self, service_name : str, *args):
        super().__init__(args)
        self._service_name = service_name

    @property
    def service_name(self):
        return self._service_name