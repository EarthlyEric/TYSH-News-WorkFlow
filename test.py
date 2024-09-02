from core.request import request
from core.config import config

decode=request.request(config.url)

sel=decode.sec