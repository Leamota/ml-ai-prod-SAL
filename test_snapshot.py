from stream.snapshot_writer import write_snapshot

sample_data = {
    "user_id": "123",
    "timestamp": "2025-10-20T22:55:00Z",
    "action": "viewed_item",
    "item_id": "abc123"
}

write_snapshot(sample_data, topic="sal.watch")
