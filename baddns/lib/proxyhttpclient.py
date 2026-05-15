import httpx

from baddns.lib.httpmanager import headers_to_dict


class ProxyResponse:
    def __init__(self, response):
        self.status = response.status_code
        self.body = response.text
        self.body_bytes = response.content
        self.headers = list(response.headers.items())
        self.url = str(response.url)
        self.elapsed_ms = int(response.elapsed.total_seconds() * 1000)
        self.redirect_chain = [str(r.url) for r in response.history]
        self.cert_info = None


class ProxyHTTPClient:
    def __init__(self, proxy_url):
        self.proxy_url = proxy_url

    async def request(self, url, method="GET", headers=None, timeout=5, verify_certs=True, follow_redirects=True):
        h = headers_to_dict(headers)
        async with httpx.AsyncClient(
            proxy=self.proxy_url,
            verify=verify_certs,
            follow_redirects=follow_redirects,
            timeout=timeout,
        ) as client:
            response = await client.request(method, url, headers=h)
            return ProxyResponse(response)
