#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
An example to show receiving events from an Event Hub with checkpoint store doing checkpoint
by every fixed event count.
In the `receive` method of `EventHubConsumerClient`:
If no partition id is specified, the checkpoint_store are used for load-balance and checkpoint.
If partition id is specified, the checkpoint_store can only be used for checkpoint.
"""
import os
from collections import defaultdict
from azure.eventhub import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblob import BlobCheckpointStore


CONNECTION_STR = os.environ["EVENT_HUB_CONN_STR"]
STORAGE_CONNECTION_STR = os.environ["AZURE_STORAGE_CONN_STR"]
BLOB_CONTAINER_NAME = "your-blob-container-name"  # Please make sure the blob container resource exists.

partition_recv_cnt_since_last_checkpoint = defaultdict(int)
checkpoint_event_cnt = 20


def on_event(partition_context, event):
    # Put your code here.
    # Avoid time-consuming operations.
    p_id = partition_context.partition_id
    print("Received event from partition: {}".format(p_id))
    partition_recv_cnt_since_last_checkpoint[p_id] += 1
    if partition_recv_cnt_since_last_checkpoint[p_id] >= checkpoint_event_cnt:
        partition_context.update_checkpoint(event)
        partition_recv_cnt_since_last_checkpoint[p_id] = 0


if __name__ == '__main__':
    checkpoint_store = BlobCheckpointStore.from_connection_string(STORAGE_CONNECTION_STR, BLOB_CONTAINER_NAME)
    consumer_client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group='$Default',
        checkpoint_store=checkpoint_store,  # For load-balancing and checkpoint. Leave None for no load-balancing.
    )

    try:
        with consumer_client:
            """
            Without specified partition_id, the receive will try to receive events from all partitions and if provided
            with a checkpoint store, the client will load-balance partition assignment with other EventHubConsumerClient
            instances which also try to receive events from all partitions and use the same storage resource.
            """
            consumer_client.receive(
                on_event=on_event,
                starting_position="-1",  # "-1" is from the beginning of the partition.
            )
            # With specified partition_id, load-balance will be disabled, for example:
            # client.receive(on_event=on_event, partition_id='0')
    except KeyboardInterrupt:
        print('Stopped receiving.')
