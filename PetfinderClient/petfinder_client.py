import requests


class PetfinderClient:

    def __init__(self, api_key: str, api_sec: str):
        self.api_key = api_key
        self.api_sec = api_sec
        self.base_url = 'https://api.petfinder.com/v2'

        self.client = requests.session()

    ERROR_DICT = {
                    401: "Unauthorized request, please check your credentials.",
                    403: "Insufficient access to the requested resource.",
                    404: "Requested resource could not be found.",
                    500: "Unexpected error - If the problem persists, please contact support."
                                }

    def _make_request(self, method, resource, **kwargs):
        url = f'{self.base_url}/{resource}'
        response = self.client.request(method, url, **kwargs)

        # Check for a successful response
        if response.status_code == 200:
            return {'success': True, 'data': response.json()}

        error_details = {
            'success': False,
            'status_code': response.status_code,
            'reason': response.reason,
            'message': self.ERROR_DICT.get(response.status_code,
                                           "An error occurred with your request."),
            'details': response.text
        }

        return error_details

    def auth(self) -> dict:
        """
        Handles initial authentication to obtain an Oauth token.
        Automatically sets it in the client's headers.

        Returns:
            dict: {
                'success',
                'data': {
                       'token_type': 'Bearer',
                       'expires_in': 3600,
                       'access_token': '<token>'
                        }
                   }
        """
        data = {'grant_type': 'client_credentials',
                'client_id': self.api_key,
                'client_secret': self.api_sec}

        response = self._make_request('POST', 'oauth2/token', json=data)

        if response['success']:
            token = response['data']['access_token']

            self.client.headers = {'Authorization': f'Bearer {token}'}

            return response
        else:
            print(f"Error: {response['data']}")

            return response

    def get_organizations_paginated(self, limit: int = 20, **kwargs) -> dict:
        """
        Returns details on a group of orgs based on given parameters.
        Pagination handled automatically.

        Args:
            limit (int, optional): Max # of results to return. Defaults to 20.

        Returns:
            dict: {
                'success': bool
                'data': {
                    'organizations': [organazitions]
                    'pagination': {pagination_dict}
                        }
                }
        """

        params = kwargs
        params['limit'] = limit

        response = self._make_request('GET', 'organizations', params=params)

        if response['success']:
            total_pages = response['data']['pagination']['total_pages']
            current_page = response['data']['pagination']['current_page']

            while current_page != total_pages:
                current_page += 1
                params['page'] = current_page
                next_response = self._make_request('GET', 'organizations', params=params)

                response['data']['organizations'].extend(next_response['data']['organizations'])
                response['data']['pagination'] = next_response['data']['pagination']

        return response

    def get_organizations(self, limit: int = 20, **kwargs) -> dict:
        """
        Returns details on a group of orgs based on given parameters.

        Args:
            limit (int, optional): Max # of results to return. Defaults to 20.

        Returns:
            dict: {
                'success': bool
                'data': {
                    'organizations': [organazitions]
                    'pagination': {pagination_dict}
                        }
                }
        """

        params = kwargs
        params['limit'] = limit

        response = self._make_request('GET', 'organizations', params=params)

        return response

    def get_organization(self, organization_id: str) -> dict:
        """
        Returns details on a single organization based on ID.

        Args:
            organization_id (str): Organization ID (obtained via get_organizations())

        Returns:
            dict: {
                'success': bool,
                'data': {
                    'organization': {organization_dict}
                    }
                }
        """

        resource = f'/organizations/{organization_id}'
        response = self._make_request('GET', resource)

        return response

    def get_animal_types(self) -> dict:
        """
        Returns array of possible animal types.

        Returns:
            dict: {
                'success': bool,
                'data': {
                    'types': [animal_lst]
                }
            }
        """

        response = self._make_request('GET', 'types')

        return response

    def get_animal_type(self) -> dict:
        """
        Returns details on a single animal type.

        Returns:
            dict: {
                'success': bool,
                'data': {
                    'type': {type_dict}
                }
            }
        """
        response = self._make_request('GET', 'type')

        return response

    def get_animal_breeds(self, animal_type: str) -> dict:
        """
        Returns possible breed values for a given animal type.

        Args:
            animal_type (str): Animal Type obtained via get_animal_types().

        Returns:
            dict: {
                'success': bool,
                'data': 'breeds': [breed_lst]
            }
        """

        resource = f'types/{animal_type}/breeds'
        response = self._make_request('GET', resource)

        return response

    def get_animals_paginated(self, **kwargs) -> dict:
        """
        Returns details on a group of animals based on given criteria.
        Handles pagination automatically.

        Returns:
            dict: {
                'success': bool,
                'data': {
                    'animals': [animal_lst],
                    'pagination': {pagination_dict}
                }
            }
        """

        params = kwargs

        response = self._make_request('GET', 'animals', params=params)

        if response['success']:
            total_pages = response['data']['pagination']['total_pages']
            current_page = response['data']['pagination']['current_page']

            while current_page != total_pages:
                current_page += 1
                params['page'] = current_page
                next_response = self._make_request('GET', 'animals', params=params)

                response['data']['animals'].extend(next_response['data']['animals'])
                response['data']['pagination'] = next_response['data']['pagination']

        return response

    def get_animals(self, **kwargs) -> dict:
        """
        Returns details on a group of animals based on given criteria.

        Returns:
            dict: {
                'success': bool,
                'data': {
                    'animals': [animal_lst],
                    'pagination': {pagination_dict}
                }
            }
        """

        response = self._make_request('GET', 'animals', params=kwargs)

        return response

    def get_animal(self, animal_id: int):
        """
        Returns details on the specified animal based on ID.

        Args:
            animal_id (int): Animal ID (obtained via get_animals())

        Returns:
            _type_: {
                'success': bool,
                'data': 'animal': {animal_dict}
            }
        """

        resource = f'animals/{animal_id}'
        response = self._make_request('GET', resource)

        return response
