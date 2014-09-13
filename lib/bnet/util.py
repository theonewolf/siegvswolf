import requests

def raw_get(conn, endpoint, **kwargs):
        kwargs['locale'] = conn.locale
        kwargs['apikey'] = conn.api_key

        r = requests.get(conn.uri + endpoint, params=kwargs)
        return r.json()
