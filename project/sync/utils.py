import re
import time
from functools import wraps


def link_to_external_id(url):
    match = re.search(r'/(\d+)/?$', url)
    return int(match.group(1)) if match else None

def retry(err=None, max_retry_count=3):
    def decorator(fn):
        @wraps(fn)
        def _wrapped_fn(*args, **kwargs):
            retry_count = 0
            while retry_count < max_retry_count:
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    retry_count += 1
                    if retry_count < max_retry_count:
                        time.sleep(retry_count ** 2)
                    else:
                        if err:
                            raise err
                        else:
                            raise e
        return _wrapped_fn
    return decorator