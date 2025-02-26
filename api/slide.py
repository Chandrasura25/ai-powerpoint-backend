from fastapi import HTTPException, APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
import openai
from pptx import Presentation
import re
import os
from Config.config import Config

router = APIRouter()

# OpenAI API Key
openai.api_key = Config.OPENAI_API_KEY

class PresentationRequest(BaseModel):
    topic: str
    num_slides: int = 5
    layout: str = "Varied"  # Default to Varied layout

@router.post("/generate-presentation")
async def generate_presentation(request: PresentationRequest):
    try:
        # Generate slide content
        slide_content = generate_slide_content(request.topic, request.num_slides)

        # Create PowerPoint presentation
        ppt = Presentation()

        for content in slide_content:
            # Select the appropriate slide layout
            if request.layout == "Varied":
                slide = ppt.slides.add_slide(ppt.slide_layouts[8])  # Image & Text
            elif request.layout == "Text-Heavy":
                slide = ppt.slides.add_slide(ppt.slide_layouts[1])  # Title & Content
            else:  # Image-Focused
                slide = ppt.slides.add_slide(ppt.slide_layouts[5])  # Title & Image

            # Add title
            if slide.shapes.title:
                slide.shapes.title.text = content["title"]

            # Handle bullet points for "Varied" and "Text-Heavy"
            if request.layout in ["Varied", "Text-Heavy"] and len(slide.placeholders) > 1:
                text_placeholder = slide.placeholders[1].text_frame
                text_placeholder.clear()

                for point in content["bullet_points"]:
                    p = text_placeholder.add_paragraph()
                    p.text = point

            # Handle Image for "Varied" and "Image-Focused"
            if request.layout in ["Varied", "Image-Focused"]:
                add_image_to_slide(slide)

        # Save the PowerPoint file
        file_path = f"{request.topic}.pptx"
        ppt.save(file_path)

        return FileResponse(file_path, filename=f"{request.topic}.pptx")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


def generate_slide_content(topic: str, num_slides: int):
    """Fetch slide content using OpenAI API."""
    try:
        prompt = f"Generate an outline for a PowerPoint presentation on '{topic}' with {num_slides} slides. Each slide should have a title and 3-5 bullet points."
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
        )

        raw_text = response.choices[0].message.content.strip()

        slides = []
        slide_texts = raw_text.split("\n\n")  # Split by double newlines

        for slide_text in slide_texts:
            lines = slide_text.split("\n")
            if not lines:
                continue

            title = re.sub(r"[*]+", "", lines[0]).strip()  # Remove `**`
            bullet_points = [re.sub(r"[*-]+", "", point).strip() for point in lines[1:] if point.strip()]

            slides.append({"title": title, "bullet_points": bullet_points})

        return slides

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


def add_image_to_slide(slide):
    """Add a sample image to the slide."""
    try:
        # get the placeholder image from the same folder
        image_path = os.path.join(os.path.dirname(__file__), "placeholder.png")

        # Add image to the slide
        left, top, width, height = 200, 150, 400, 300
        slide.shapes.add_picture(image_path, left, top, width, height)

    except Exception:
        pass  # Ignore image errors if any occur
