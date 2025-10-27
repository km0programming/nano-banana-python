import argparse
import mimetypes
import os
import time
import google.generativeai as genai
# We no longer need to import 'types' separately as Part/Blob are directly under genai
# from google.generativeai import types
from dotenv import load_dotenv
import urllib3
from PIL import Image

# 2. AÑADE ESTAS LÍNEAS PARA SILENCIAR EL AVISO DE SEGURIDAD
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables from .env file
load_dotenv()

MODEL_NAME = "gemini-2.5-flash-image-preview"

def remix_images(
    image_paths: list[str],
    prompt: str,
    output_dir: str,
):
    """
    Remixes one or more images using the Google Generative AI model.

    Args:
        image_paths: A list of paths to input images.
        prompt: The prompt for remixing the images.
        output_dir: Directory to save the remixed images.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable not set. "
            "Please ensure you have a .env file with GEMINI_API_KEY='your_api_key' "
            "or set it in your system environment."
        )

    try:
        genai.configure(api_key=api_key)
        print("Generative AI configured successfully.")
    except Exception as e:
        print(f"Error configuring Generative AI: {e}")
        return None

    contents = _load_image_parts(image_paths)
    # Corrected: Use genai.Part directly
    contents.append(genai.Part.from_text(text=prompt))

    generate_content_config = genai.types.GenerateContentConfig( # Still use genai.types for GenerateContentConfig
        response_modalities=["IMAGE", "TEXT"],
    )

    print(f"Remixing with {len(image_paths)} image(s) and prompt: '{prompt}' using model: {MODEL_NAME}")

    try:
        model = genai.GenerativeModel(MODEL_NAME)

        stream = model.generate_content(
            contents=contents,
            generation_config=generate_content_config,
            stream=True
        )

        _process_api_stream_response(stream, output_dir)

    except Exception as e:
        print(f"Error during content generation: {e}")

# Corrected: Update the type hint to use genai.Part
def _load_image_parts(image_paths: list[str]) -> list[genai.Part]:
    """Loads image files and converts them into GenAI Part objects."""
    parts = []
    for image_path in image_paths:
        if not os.path.exists(image_path):
            print(f"Warning: Image file '{image_path}' not found. Attempting to create a dummy placeholder.")
            try:
                img = Image.new('RGB', (100, 100), color = 'red')
                img.save(image_path)
                print(f"Dummy image '{image_path}' created. For better results, provide a real image.")
            except ImportError:
                print("Pillow library not found. Cannot create dummy image. Please install it (`pip install Pillow`) or provide a real image file.")
                raise FileNotFoundError(f"Image file '{image_path}' not found and Pillow not available to create dummy.")

        with open(image_path, "rb") as f:
            image_data = f.read()
        mime_type = _get_mime_type(image_path)
        parts.append(
            # Corrected: Use genai.Part and genai.types.Blob (Blob is in types)
            genai.Part(inline_data=genai.types.Blob(data=image_data, mime_type=mime_type))
        )
    return parts


def _process_api_stream_response(stream, output_dir: str):
    """Processes the streaming response from the GenAI API, saving images and printing text."""
    file_index = 0
    print("\n--- Processing API Response Stream ---")
    for chunk in stream:
        if not chunk.candidates or not chunk.candidates[0].content:
            print("Received empty chunk or no content in candidate.")
            continue

        for part in chunk.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                timestamp = int(time.time())
                file_extension = mimetypes.guess_extension(part.inline_data.mime_type)
                if not file_extension:
                    file_extension = ".jpg"
                file_name = os.path.join(
                    output_dir,
                    f"remixed_image_{timestamp}_{file_index}{file_extension}",
                )
                _save_binary_file(file_name, part.inline_data.data)
                file_index += 1
            elif part.text:
                print(f"Model Text Response: {part.text}")
            else:
                print(f"Received unknown part type: {type(part)}")
    print("\n--- Stream Processing Complete ---")


def _save_binary_file(file_name: str, data: bytes):
    """Saves binary data to a specified file."""
    try:
        with open(file_name, "wb") as f:
            f.write(data)
        print(f"File saved to: {file_name}")
    except IOError as e:
        print(f"Error saving file '{file_name}': {e}")


def _get_mime_type(file_path: str) -> str:
    """Guesses the MIME type of a file based on its extension."""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".jpg" or ext == ".jpeg":
            return "image/jpeg"
        elif ext == ".png":
            return "image/png"
        elif ext == ".gif":
            return "image/gif"
        raise ValueError(f"Could not determine MIME type for {file_path}. Please ensure it's a common image format.")
    return mime_type


def main():
    parser = argparse.ArgumentParser(
        description="Remix images using Google Generative AI."
    )
    parser.add_argument(
        "-i",
        "--image",
        action="append",
        required=True,
        help="Paths to input images (1-5 images). Provide multiple -i flags for multiple images.",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="Optional prompt for remixing the images.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory to save the remixed images.",
    )

    args = parser.parse_args()

    all_image_paths = args.image

    num_images = len(all_image_paths)
    if not (1 <= num_images <= 5):
        parser.error("Please provide between 1 and 5 input images using the -i flag.")

    final_prompt = args.prompt
    if final_prompt is None:
        if num_images == 1:
            final_prompt = "Turn this image into a professional quality studio shoot with better lighting and depth of field, with a modern aesthetic."
        else:
            final_prompt = "Combine the subjects of these images in a natural way, producing a new, cohesive image. Maintain the style and lighting of the first image."

    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    remix_images(
        image_paths=all_image_paths,
        prompt=final_prompt,
        output_dir=output_dir,
    )


if __name__ == "__main__":
    main()