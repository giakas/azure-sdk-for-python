# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: identity_sample.py
DESCRIPTION:
    These samples demonstrate identity client samples.

    ///authenticating a client via a connection string
USAGE:
    python identity_samples.py
"""
import os

class CommunicationIdentityClientSamples(object):

    def __init__(self):
        self.connection_string = os.getenv('AZURE_COMMUNICATION_SERVICE_CONNECTION_STRING')
        self.endpoint = os.getenv('AZURE_COMMUNICATION_SERVICE_ENDPOINT')
        self.client_id = os.getenv('AZURE_CLIENT_ID')
        self.client_secret = os.getenv('AZURE_CLIENT_SECRET')
        self.tenant_id = os.getnenv('AZURE_TENANT_ID')

    def issue_token(self):
        from azure.communication.administration import CommunicationIdentityClient

        if self.client_id is not None and self.client_secret is not None and self.tenant_id is not None:
            from azure.identity import DefaultAzureCredential
            identity_client = CommunicationIdentityClient(self.endpoint, DefaultAzureCredential())
        else:
            identity_client = CommunicationIdentityClient.from_connection_string(self.connection_string)
        user = identity_client.create_user()
        tokenresponse = identity_client.issue_token(user, scopes=["chat"])
        print(tokenresponse)
    
    def revoke_tokens(self):
        from azure.communication.administration import CommunicationIdentityClient

        if self.client_id is not None and self.client_secret is not None and self.tenant_id is not None:
            from azure.identity import DefaultAzureCredential
            identity_client = CommunicationIdentityClient(self.endpoint, DefaultAzureCredential())
        else:
            identity_client = CommunicationIdentityClient.from_connection_string(self.connection_string)
        user = identity_client.create_user()
        tokenresponse = identity_client.issue_token(user, scopes=["chat"])
        identity_client.revoke_tokens(user)
        print(tokenresponse)

    def create_user(self):
        from azure.communication.administration import CommunicationIdentityClient

        if self.client_id is not None and self.client_secret is not None and self.tenant_id is not None:
            from azure.identity import DefaultAzureCredential
            identity_client = CommunicationIdentityClient(self.endpoint, DefaultAzureCredential())
        else:
            identity_client = CommunicationIdentityClient.from_connection_string(self.connection_string)
        user = identity_client.create_user()
        print(user.identifier)
    
    def delete_user(self):
        from azure.communication.administration import CommunicationIdentityClient

        if self.client_id is not None and self.client_secret is not None and self.tenant_id is not None:
            from azure.identity import DefaultAzureCredential
            identity_client = CommunicationIdentityClient(self.endpoint, DefaultAzureCredential())
        else:
            identity_client = CommunicationIdentityClient.from_connection_string(self.connection_string)
        user = identity_client.create_user()
        identity_client.delete_user(user)

if __name__ == '__main__':
    sample = CommunicationIdentityClientSamples()
    sample.create_user()
    sample.delete_user()
    sample.issue_token()
    sample.revoke_tokens()
