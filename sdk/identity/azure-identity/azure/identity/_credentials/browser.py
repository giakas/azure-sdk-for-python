# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import socket
import uuid
import webbrowser

from six.moves.urllib_parse import urlparse

from azure.core.exceptions import ClientAuthenticationError

from .. import CredentialUnavailableError
from .._constants import DEVELOPER_SIGN_ON_CLIENT_ID
from .._internal import AuthCodeRedirectServer, InteractiveCredential, wrap_exceptions

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    # pylint:disable=unused-import
    from typing import Any, List, Mapping


class InteractiveBrowserCredential(InteractiveCredential):
    """Opens a browser to interactively authenticate a user.

    :func:`~get_token` opens a browser to a login URL provided by Azure Active Directory and authenticates a user
    there with the authorization code flow. Azure Active Directory documentation describes this flow in more detail:
    https://docs.microsoft.com/azure/active-directory/develop/v1-protocols-oauth-code

    :keyword str authority: Authority of an Azure Active Directory endpoint, for example 'login.microsoftonline.com',
          the authority for Azure Public Cloud (which is the default). :class:`~azure.identity.AzureAuthorityHosts`
          defines authorities for other clouds.
    :keyword str tenant_id: an Azure Active Directory tenant ID. Defaults to the 'organizations' tenant, which can
          authenticate work or school accounts.
    :keyword str client_id: Client ID of the Azure Active Directory application users will sign in to. If
          unspecified, users will authenticate to an Azure development application.
    :keyword str redirect_uri: a redirect URI for the application identified by `client_id` as configured in Azure
          Active Directory, for example "http://localhost:8400". This is only required when passing a value for
          `client_id`, and must match a redirect URI in the application's registration. The credential must be able to
          bind a socket to this URI.
    :keyword AuthenticationRecord authentication_record: :class:`AuthenticationRecord` returned by :func:`authenticate`
    :keyword bool disable_automatic_authentication: if True, :func:`get_token` will raise
          :class:`AuthenticationRequiredError` when user interaction is required to acquire a token. Defaults to False.
    :keyword bool enable_persistent_cache: if True, the credential will store tokens in a persistent cache shared by
         other user credentials. Defaults to False.
    :keyword bool allow_unencrypted_cache: if True, the credential will fall back to a plaintext cache on platforms
          where encryption is unavailable. Default to False. Has no effect when `enable_persistent_cache` is False.
    :keyword int timeout: seconds to wait for the user to complete authentication. Defaults to 300 (5 minutes).
    :raises ValueError: invalid `redirect_uri`
    """

    def __init__(self, **kwargs):
        # type: (**Any) -> None
        redirect_uri = kwargs.pop("redirect_uri", None)
        if redirect_uri:
            self._parsed_url = urlparse(redirect_uri)
            if not (self._parsed_url.hostname and self._parsed_url.port):
                raise ValueError('"redirect_uri" must be a URL with port number, for example "http://localhost:8400"')
        else:
            self._parsed_url = None

        self._timeout = kwargs.pop("timeout", 300)
        self._server_class = kwargs.pop("_server_class", AuthCodeRedirectServer)
        client_id = kwargs.pop("client_id", DEVELOPER_SIGN_ON_CLIENT_ID)
        super(InteractiveBrowserCredential, self).__init__(client_id=client_id, **kwargs)

    @wrap_exceptions
    def _request_token(self, *scopes, **kwargs):
        # type: (*str, **Any) -> dict

        # start an HTTP server to receive the redirect
        server = None
        if self._parsed_url:
            try:
                redirect_uri = "http://{}:{}".format(self._parsed_url.hostname, self._parsed_url.port)
                server = self._server_class(self._parsed_url.hostname, self._parsed_url.port, timeout=self._timeout)
            except socket.error:
                raise CredentialUnavailableError(message="Couldn't start an HTTP server on " + redirect_uri)
        else:
            for port in range(8400, 9000):
                try:
                    server = self._server_class("localhost", port, timeout=self._timeout)
                    redirect_uri = "http://localhost:{}".format(port)
                    break
                except socket.error:
                    continue  # keep looking for an open port

        if not server:
            raise CredentialUnavailableError(message="Couldn't start an HTTP server on localhost")

        # get the url the user must visit to authenticate
        scopes = list(scopes)  # type: ignore
        request_state = str(uuid.uuid4())
        app = self._get_app()
        auth_url = app.get_authorization_request_url(
            scopes, redirect_uri=redirect_uri, state=request_state, prompt="select_account", **kwargs
        )

        # open browser to that url
        if not webbrowser.open(auth_url):
            raise CredentialUnavailableError(message="Failed to open a browser")

        # block until the server times out or receives the post-authentication redirect
        response = server.wait_for_redirect()
        if not response:
            raise ClientAuthenticationError(
                message="Timed out after waiting {} seconds for the user to authenticate".format(self._timeout)
            )

        # redeem the authorization code for a token
        code = self._parse_response(request_state, response)
        return app.acquire_token_by_authorization_code(code, scopes=scopes, redirect_uri=redirect_uri, **kwargs)

    @staticmethod
    def _parse_response(request_state, response):
        # type: (str, Mapping[str, Any]) -> List[str]
        """Validates ``response`` and returns the authorization code it contains, if authentication succeeded.

        Raises :class:`azure.core.exceptions.ClientAuthenticationError`, if authentication failed or ``response`` is
        malformed.
        """

        if "error" in response:
            message = "Authentication failed: {}".format(response.get("error_description") or response["error"])
            raise ClientAuthenticationError(message=message)
        if "code" not in response:
            # a response with no error or code is malformed; we don't know what to do with it
            message = "Authentication server didn't send an authorization code"
            raise ClientAuthenticationError(message=message)

        # response must include the state sent in the auth request
        if "state" not in response:
            raise ClientAuthenticationError(message="Authentication response doesn't include OAuth state")
        if response["state"][0] != request_state:
            raise ClientAuthenticationError(message="Authentication response's OAuth state doesn't match the request's")

        return response["code"]
