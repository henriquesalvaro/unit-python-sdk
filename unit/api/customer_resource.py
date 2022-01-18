from unit.api.base_resource import BaseResource
from unit.models.customer import *
from unit.models.codecs import DtoDecoder


class CustomerResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "customers"

    def update(self, request: Union[PatchIndividualCustomerRequest, PatchBusinessCustomerRequest]) -> Union[UnitResponse[CustomerDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"{self.resource}/{request.customer_id}", payload)

        if response.ok:
            data = response.json().get("data")
            if data["type"] == "individualCustomer":
                return UnitResponse[IndividualCustomerDTO](DtoDecoder.decode(data), None)
            else:
                return UnitResponse[BusinessCustomerDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())


    def get(self, customer_id: str) -> Union[UnitResponse[CustomerDTO], UnitError]:
        response = super().get(f"{self.resource}/{customer_id}")
        if response.status_code == 200:
            data = response.json().get("data")
            return UnitResponse[CustomerDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListCustomerParams = ListCustomerParams()) -> Union[UnitResponse[List[CustomerDTO]], UnitError]:
        parameters = {"page[limit]": params.limit, "page[offset]": params.offset, "sort": params.sort}

        if params.query:
            parameters["filter[query]"] = params.query

        if params.email:
            parameters["filter[email]"] = params.email

        if params.tags:
            parameters["filter[tags]"] = params.tags

        response = super().get(self.resource, parameters)
        if response.status_code == 200:
            data = response.json().get("data")
            return UnitResponse[CustomerDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
