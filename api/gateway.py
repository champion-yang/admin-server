from .base import BaseServiceAPI
from configuration import config_obj


class GatewayService(BaseServiceAPI):

    def get_base_url(self):
        return config_obj.get("gateway", "base_url")
