
import json
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from vsg_themes import vsg_themes_route
from vsg_themes.utils import VSGThemesModels, get_settings

# start the API
settings = get_settings()


# Prepare context
@asynccontextmanager
async def lifespan(app: FastAPI):
    # -------------------------------------
    # load AI Model
    # for now, we will opt to load during API startup to avoid too much I/O on loading/unloading big files
    # and thus setting the model as a global var
    app.state.settings = settings
    themes_utils = (
        VSGThemesModels(settings['vsg_services']['themes']['method'])
    )
    themes_utils.load_all_models()
    app.state.models = themes_utils
    yield
    app.state.settings = []

print(json.dumps(settings, indent=4))

app = FastAPI(
    title=settings['vsg_services']['themes']['api_title'],
    description=settings['vsg_services']['themes']['api_description'],
    version=settings['vsg_services']['themes']['api_version'],
    docs_url=settings['vsg_services']['themes']['docs_url'],
    lifespan=lifespan
)

# Establish routers
app.include_router(vsg_themes_route.router)


@app.get('/version')
async def version():
    return {"message": f"I am running version {settings['vsg_services']['themes']['api_version']}"}

if __name__ == '__main__':
    uvicorn.run(
        app,
        port=settings['vsg_services']['themes']['local']['port'],
        host=settings['vsg_services']['themes']['local']['host'])
