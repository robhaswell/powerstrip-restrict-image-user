import json as _json

def pre_hook_response(method, path, json):
    """
    Format a Powerstrip pre-hook response JSON blob.
    """
    return _json.dumps(dict(
        PowerstripProtocolVersion=1,
        ModifiedClientRequest=dict(
            Method=method,
            Request=path,
            Body=json,
        )))


