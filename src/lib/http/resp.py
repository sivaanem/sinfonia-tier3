import requests


def is_success_status_code(status_code: int) -> bool:
    return status_code >= 200 and status_code <= 299
    
    
def is_json_response(resp: requests.Response) -> bool:
    """Check if response is of JSON type. 
    
    Args:
        resp -- requests.Response: Response object
        
    Return:
        bool
    """
    try:
        _ = resp.json()
        return True
    except:
        return False
    
    # resp.headers.get('content-type') == 'application/json' 
    