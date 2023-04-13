#!/usr/bin/env bash
SOLARA_APP=domino_code_assist.app_entrypoint SOLARA_TELEMETRY_MIXPANEL_ENABLE=False SOLARA_THEME_VARIANT=light\
    SOLARA_THEME_LOADER=plain uvicorn solara.server.starlette:app\
    --loop asyncio\
    --host=0.0.0.0 --port=8888