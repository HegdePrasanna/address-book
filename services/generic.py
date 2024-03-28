from fastapi import Request


async def get_client_ip(request: Request):
    """
    Get the IP address from where request is being made
    """
    client_host = request.client.host
    return client_host