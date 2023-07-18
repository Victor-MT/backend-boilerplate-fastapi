from fastapi import Request
import inspect

from database.database import get_db
from .logger import logger
from datetime import datetime
from fastapi.responses import JSONResponse
from database.models.models import BotLog

async def add_custom_logger(request: Request, call_next):
    start_time = datetime.now()
    logger.info(f"[REQUEST] ROUTE PATH: {request.method} {request.url.path}")

    db = get_db()
    session = next(db)

    if '/pipeline' in request.url.path:
        logger.set_bot_log()

    try:
        request.state.db = session
        response = await call_next(request)
        session.commit()

    except Exception as e:
        session.rollback()

        logger.error(f"[REQUEST] Exception occurred: {e}")
        response = JSONResponse(
                                status_code=500, 
                                content= { "error": f"{e}" })
    finally:

        end_time = datetime.now()
        elapsed_time = end_time - start_time
        logger.info(f"[REQUEST] EndTime: {elapsed_time}")
        logger.info(f"[REQUEST] Status: {response.status_code}")
        logger.close()

    return response