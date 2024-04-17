import traceback
from fastapi import APIRouter, Body, HTTPException, status, Request

from vsg_utils.vsg_api_schema import ThemesRequest
from vsg_themes.utils import VSGThemesModels

router = APIRouter(prefix="/themes")


async def run_predict(content: str, models: VSGThemesModels):
    return models.model.conduct_analysis_and_create_report(data=content)


@router.post(
    "/predict",
    status_code=status.HTTP_200_OK,
    summary="Predict themes.",
    response_description="Returns the prediction of themes."
)
async def predict_themes(
        request: Request,
        body: ThemesRequest = Body(
            ..., example={"content": "String"}
        )
):
    models = request.app.state.models

    try:
        response = await run_predict(
            content=body.content,
            models=models
        )
        return response

    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=traceback.format_exc()
        ) from ex

