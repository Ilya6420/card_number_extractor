from io import BytesIO

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

from core.logging_config import get_logger
from schemas.card_number import CardNumberOutput
from services.card_number import card_number_extractor


router = APIRouter()

logger = get_logger(__name__)


@router.post("/predict", response_model=CardNumberOutput)
async def predict(file: UploadFile = File(...)):
    logger.info(f"Received request to predict card number from file: {file.filename}")
    try:
        # Read the image file
        logger.debug("Reading uploaded file contents")
        image = Image.open(BytesIO(await file.read()))

        # Process the image using the singleton extractor
        logger.info("Processing image with card number extractor")
        card_number, bbox, confidence = card_number_extractor.extract_card_number(image)
        print(card_number, bbox, confidence)
        if card_number:
            logger.info(f"Successfully extracted card number: {card_number[:4]}****{card_number[-4:]}")
            return CardNumberOutput(
                card_number=card_number,
                bbox=bbox,
                confidence=confidence
            )
        else:
            logger.warning("No valid card number found in the image")
            return JSONResponse(
                status_code=400,
                content={"message": "No valid card number found in the image"}
            )

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=400,
            content={"message": f"Error processing image: {str(e)}"}
        )
