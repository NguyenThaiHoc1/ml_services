"""
[Summary] APIs
[Information]
    @author: Nguyen Thai Hoc
    @email: nguyenthaihoc1996@outlook.com
    @create: 27-09-2022
"""
import logging
from logging.handlers import TimedRotatingFileHandler
from fastapi import FastAPI
from settings import config
from api_endpoint.routers import api_routers

# DEFINE API
app = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/openapi.json", docs_url="/api/docs", redoc_url="/api/redoc")

# HANDLE LOG FILE Sẽ xem lại cái này
formatter = logging.Formatter("%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s")
handler = TimedRotatingFileHandler(config.PATH_PROJECT / 'logs' / '{}-{}-{}_{}h-00p-00.log'.format(
    config.universal.year,
    config.universal.month,
    config.universal.day,
    config.universal.hour), when="midnight", interval=1, encoding="utf-8")

handler.suffix = "%Y-%m-%d"
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(level=logging.DEBUG)
logger.addHandler(handler)

# ROUTER CONFIG
app.include_router(api_routers, prefix="/api/v1")
