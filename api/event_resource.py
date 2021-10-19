from api.base_resource import BaseResource
from models.event import *
from models.codecs import DtoDecoder


class EventResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "events"

    def get(self, event_id: str) -> Union[UnitResponse[EventDTO], UnitError]:
        response = super().get(f"{self.resource}/{event_id}")
        if response.status_code == 200:
            data = response.json().get("data")
            return UnitResponse[EventDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self, offset: int = 0, limit: int = 100) -> Union[UnitResponse[list[EventDTO]], UnitError]:
        response = super().get(self.resource, {"page[limit]": limit, "page[offset]": offset})
        if response.status_code == 200:
            data = response.json().get("data")
            return UnitResponse[EventDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
