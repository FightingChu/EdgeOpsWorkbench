"""Deterministic protocol version and feature negotiation."""


def negotiate(peer_versions, peer_features, *, supported_versions=(1,), supported_features=("reading", "ack")):
    if not isinstance(peer_versions, list) or not peer_versions or not all(type(item) is int for item in peer_versions):
        raise ValueError("peer_versions must be a nonempty integer list")
    common = sorted(set(peer_versions) & set(supported_versions), reverse=True)
    if not common:
        raise ValueError("no compatible protocol version")
    if not isinstance(peer_features, list) or not all(isinstance(item, str) for item in peer_features):
        raise ValueError("peer_features must be text values")
    return {"version": common[0], "features": sorted(set(peer_features) & set(supported_features))}
