# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import TYPE_CHECKING
import warnings

from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.paging import ItemPaged
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import HttpRequest, HttpResponse
from azure.mgmt.core.exceptions import ARMErrorFormat

from .. import models

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from typing import Any, Callable, Dict, Generic, Iterable, Optional, TypeVar, Union

    T = TypeVar('T')
    ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

class PolicySetDefinitionsOperations(object):
    """PolicySetDefinitionsOperations operations.

    You should not instantiate this class directly. Instead, you should create a Client instance that
    instantiates it for you and attaches it as an attribute.

    :ivar models: Alias to model classes used in this operation group.
    :type models: ~azure.mgmt.resource.policy.v2019_09_01.models
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = models

    def __init__(self, client, config, serializer, deserializer):
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self._config = config

    def create_or_update(
        self,
        policy_set_definition_name,  # type: str
        parameters,  # type: "models.PolicySetDefinition"
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.PolicySetDefinition"
        """Creates or updates a policy set definition.

        This operation creates or updates a policy set definition in the given subscription with the
        given name.

        :param policy_set_definition_name: The name of the policy set definition to create.
        :type policy_set_definition_name: str
        :param parameters: The policy set definition properties.
        :type parameters: ~azure.mgmt.resource.policy.v2019_09_01.models.PolicySetDefinition
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: PolicySetDefinition, or the result of cls(response)
        :rtype: ~azure.mgmt.resource.policy.v2019_09_01.models.PolicySetDefinition
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.PolicySetDefinition"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2019-09-01"
        content_type = kwargs.pop("content_type", "application/json")
        accept = "application/json"

        # Construct URL
        url = self.create_or_update.metadata['url']  # type: ignore
        path_format_arguments = {
            'policySetDefinitionName': self._serialize.url("policy_set_definition_name", policy_set_definition_name, 'str'),
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        body_content_kwargs = {}  # type: Dict[str, Any]
        body_content = self._serialize.body(parameters, 'PolicySetDefinition')
        body_content_kwargs['content'] = body_content
        request = self._client.put(url, query_parameters, header_parameters, **body_content_kwargs)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200, 201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        if response.status_code == 200:
            deserialized = self._deserialize('PolicySetDefinition', pipeline_response)

        if response.status_code == 201:
            deserialized = self._deserialize('PolicySetDefinition', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    create_or_update.metadata = {'url': '/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName}'}  # type: ignore

    def delete(
        self,
        policy_set_definition_name,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Deletes a policy set definition.

        This operation deletes the policy set definition in the given subscription with the given name.

        :param policy_set_definition_name: The name of the policy set definition to delete.
        :type policy_set_definition_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2019-09-01"
        accept = "application/json"

        # Construct URL
        url = self.delete.metadata['url']  # type: ignore
        path_format_arguments = {
            'policySetDefinitionName': self._serialize.url("policy_set_definition_name", policy_set_definition_name, 'str'),
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        request = self._client.delete(url, query_parameters, header_parameters)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200, 204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        if cls:
            return cls(pipeline_response, None, {})

    delete.metadata = {'url': '/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName}'}  # type: ignore

    def get(
        self,
        policy_set_definition_name,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.PolicySetDefinition"
        """Retrieves a policy set definition.

        This operation retrieves the policy set definition in the given subscription with the given
        name.

        :param policy_set_definition_name: The name of the policy set definition to get.
        :type policy_set_definition_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: PolicySetDefinition, or the result of cls(response)
        :rtype: ~azure.mgmt.resource.policy.v2019_09_01.models.PolicySetDefinition
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.PolicySetDefinition"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2019-09-01"
        accept = "application/json"

        # Construct URL
        url = self.get.metadata['url']  # type: ignore
        path_format_arguments = {
            'policySetDefinitionName': self._serialize.url("policy_set_definition_name", policy_set_definition_name, 'str'),
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        request = self._client.get(url, query_parameters, header_parameters)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('PolicySetDefinition', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    get.metadata = {'url': '/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName}'}  # type: ignore

    def get_built_in(
        self,
        policy_set_definition_name,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.PolicySetDefinition"
        """Retrieves a built in policy set definition.

        This operation retrieves the built-in policy set definition with the given name.

        :param policy_set_definition_name: The name of the policy set definition to get.
        :type policy_set_definition_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: PolicySetDefinition, or the result of cls(response)
        :rtype: ~azure.mgmt.resource.policy.v2019_09_01.models.PolicySetDefinition
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.PolicySetDefinition"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2019-09-01"
        accept = "application/json"

        # Construct URL
        url = self.get_built_in.metadata['url']  # type: ignore
        path_format_arguments = {
            'policySetDefinitionName': self._serialize.url("policy_set_definition_name", policy_set_definition_name, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        request = self._client.get(url, query_parameters, header_parameters)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('PolicySetDefinition', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    get_built_in.metadata = {'url': '/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName}'}  # type: ignore

    def list(
        self,
        **kwargs  # type: Any
    ):
        # type: (...) -> Iterable["models.PolicySetDefinitionListResult"]
        """Retrieves the policy set definitions for a subscription.

        This operation retrieves a list of all the policy set definitions in the given subscription.

        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either PolicySetDefinitionListResult or the result of cls(response)
        :rtype: ~azure.core.paging.ItemPaged[~azure.mgmt.resource.policy.v2019_09_01.models.PolicySetDefinitionListResult]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.PolicySetDefinitionListResult"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2019-09-01"
        accept = "application/json"

        def prepare_request(next_link=None):
            # Construct headers
            header_parameters = {}  # type: Dict[str, Any]
            header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

            if not next_link:
                # Construct URL
                url = self.list.metadata['url']  # type: ignore
                path_format_arguments = {
                    'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
                }
                url = self._client.format_url(url, **path_format_arguments)
                # Construct parameters
                query_parameters = {}  # type: Dict[str, Any]
                query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

                request = self._client.get(url, query_parameters, header_parameters)
            else:
                url = next_link
                query_parameters = {}  # type: Dict[str, Any]
                request = self._client.get(url, query_parameters, header_parameters)
            return request

        def extract_data(pipeline_response):
            deserialized = self._deserialize('PolicySetDefinitionListResult', pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, iter(list_of_elem)

        def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, error_format=ARMErrorFormat)

            return pipeline_response

        return ItemPaged(
            get_next, extract_data
        )
    list.metadata = {'url': '/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policySetDefinitions'}  # type: ignore

    def list_built_in(
        self,
        **kwargs  # type: Any
    ):
        # type: (...) -> Iterable["models.PolicySetDefinitionListResult"]
        """Retrieves built-in policy set definitions.

        This operation retrieves a list of all the built-in policy set definitions.

        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either PolicySetDefinitionListResult or the result of cls(response)
        :rtype: ~azure.core.paging.ItemPaged[~azure.mgmt.resource.policy.v2019_09_01.models.PolicySetDefinitionListResult]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.PolicySetDefinitionListResult"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2019-09-01"
        accept = "application/json"

        def prepare_request(next_link=None):
            # Construct headers
            header_parameters = {}  # type: Dict[str, Any]
            header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

            if not next_link:
                # Construct URL
                url = self.list_built_in.metadata['url']  # type: ignore
                # Construct parameters
                query_parameters = {}  # type: Dict[str, Any]
                query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

                request = self._client.get(url, query_parameters, header_parameters)
            else:
                url = next_link
                query_parameters = {}  # type: Dict[str, Any]
                request = self._client.get(url, query_parameters, header_parameters)
            return request

        def extract_data(pipeline_response):
            deserialized = self._deserialize('PolicySetDefinitionListResult', pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, iter(list_of_elem)

        def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, error_format=ARMErrorFormat)

            return pipeline_response

        return ItemPaged(
            get_next, extract_data
        )
    list_built_in.metadata = {'url': '/providers/Microsoft.Authorization/policySetDefinitions'}  # type: ignore

    def create_or_update_at_management_group(
        self,
        policy_set_definition_name,  # type: str
        management_group_id,  # type: str
        parameters,  # type: "models.PolicySetDefinition"
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.PolicySetDefinition"
        """Creates or updates a policy set definition.

        This operation creates or updates a policy set definition in the given management group with
        the given name.

        :param policy_set_definition_name: The name of the policy set definition to create.
        :type policy_set_definition_name: str
        :param management_group_id: The ID of the management group.
        :type management_group_id: str
        :param parameters: The policy set definition properties.
        :type parameters: ~azure.mgmt.resource.policy.v2019_09_01.models.PolicySetDefinition
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: PolicySetDefinition, or the result of cls(response)
        :rtype: ~azure.mgmt.resource.policy.v2019_09_01.models.PolicySetDefinition
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.PolicySetDefinition"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2019-09-01"
        content_type = kwargs.pop("content_type", "application/json")
        accept = "application/json"

        # Construct URL
        url = self.create_or_update_at_management_group.metadata['url']  # type: ignore
        path_format_arguments = {
            'policySetDefinitionName': self._serialize.url("policy_set_definition_name", policy_set_definition_name, 'str'),
            'managementGroupId': self._serialize.url("management_group_id", management_group_id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        body_content_kwargs = {}  # type: Dict[str, Any]
        body_content = self._serialize.body(parameters, 'PolicySetDefinition')
        body_content_kwargs['content'] = body_content
        request = self._client.put(url, query_parameters, header_parameters, **body_content_kwargs)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200, 201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        if response.status_code == 200:
            deserialized = self._deserialize('PolicySetDefinition', pipeline_response)

        if response.status_code == 201:
            deserialized = self._deserialize('PolicySetDefinition', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    create_or_update_at_management_group.metadata = {'url': '/providers/Microsoft.Management/managementgroups/{managementGroupId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName}'}  # type: ignore

    def delete_at_management_group(
        self,
        policy_set_definition_name,  # type: str
        management_group_id,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Deletes a policy set definition.

        This operation deletes the policy set definition in the given management group with the given
        name.

        :param policy_set_definition_name: The name of the policy set definition to delete.
        :type policy_set_definition_name: str
        :param management_group_id: The ID of the management group.
        :type management_group_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2019-09-01"
        accept = "application/json"

        # Construct URL
        url = self.delete_at_management_group.metadata['url']  # type: ignore
        path_format_arguments = {
            'policySetDefinitionName': self._serialize.url("policy_set_definition_name", policy_set_definition_name, 'str'),
            'managementGroupId': self._serialize.url("management_group_id", management_group_id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        request = self._client.delete(url, query_parameters, header_parameters)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200, 204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        if cls:
            return cls(pipeline_response, None, {})

    delete_at_management_group.metadata = {'url': '/providers/Microsoft.Management/managementgroups/{managementGroupId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName}'}  # type: ignore

    def get_at_management_group(
        self,
        policy_set_definition_name,  # type: str
        management_group_id,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.PolicySetDefinition"
        """Retrieves a policy set definition.

        This operation retrieves the policy set definition in the given management group with the given
        name.

        :param policy_set_definition_name: The name of the policy set definition to get.
        :type policy_set_definition_name: str
        :param management_group_id: The ID of the management group.
        :type management_group_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: PolicySetDefinition, or the result of cls(response)
        :rtype: ~azure.mgmt.resource.policy.v2019_09_01.models.PolicySetDefinition
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.PolicySetDefinition"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2019-09-01"
        accept = "application/json"

        # Construct URL
        url = self.get_at_management_group.metadata['url']  # type: ignore
        path_format_arguments = {
            'policySetDefinitionName': self._serialize.url("policy_set_definition_name", policy_set_definition_name, 'str'),
            'managementGroupId': self._serialize.url("management_group_id", management_group_id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        request = self._client.get(url, query_parameters, header_parameters)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('PolicySetDefinition', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    get_at_management_group.metadata = {'url': '/providers/Microsoft.Management/managementgroups/{managementGroupId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName}'}  # type: ignore

    def list_by_management_group(
        self,
        management_group_id,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> Iterable["models.PolicySetDefinitionListResult"]
        """Retrieves all policy set definitions in management group.

        This operation retrieves a list of all the a policy set definition in the given management
        group.

        :param management_group_id: The ID of the management group.
        :type management_group_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either PolicySetDefinitionListResult or the result of cls(response)
        :rtype: ~azure.core.paging.ItemPaged[~azure.mgmt.resource.policy.v2019_09_01.models.PolicySetDefinitionListResult]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.PolicySetDefinitionListResult"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2019-09-01"
        accept = "application/json"

        def prepare_request(next_link=None):
            # Construct headers
            header_parameters = {}  # type: Dict[str, Any]
            header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

            if not next_link:
                # Construct URL
                url = self.list_by_management_group.metadata['url']  # type: ignore
                path_format_arguments = {
                    'managementGroupId': self._serialize.url("management_group_id", management_group_id, 'str'),
                }
                url = self._client.format_url(url, **path_format_arguments)
                # Construct parameters
                query_parameters = {}  # type: Dict[str, Any]
                query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

                request = self._client.get(url, query_parameters, header_parameters)
            else:
                url = next_link
                query_parameters = {}  # type: Dict[str, Any]
                request = self._client.get(url, query_parameters, header_parameters)
            return request

        def extract_data(pipeline_response):
            deserialized = self._deserialize('PolicySetDefinitionListResult', pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, iter(list_of_elem)

        def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, error_format=ARMErrorFormat)

            return pipeline_response

        return ItemPaged(
            get_next, extract_data
        )
    list_by_management_group.metadata = {'url': '/providers/Microsoft.Management/managementgroups/{managementGroupId}/providers/Microsoft.Authorization/policySetDefinitions'}  # type: ignore
