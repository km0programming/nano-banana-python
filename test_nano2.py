import google.generativeai as genai
import os
import io
from PIL import Image

api_key = "AIzaSyB-KiR83uGM7z_P7RdFbVinn7Wsi7VzRVw"

# --- Configuration ---
# api_key = os.getenv("GOOGLE_API_KEY") # Ensure this is your API key for prjnanobanano

if not api_key:
    print("API Key not found. Please set the GOOGLE_API_KEY environment variable or hardcode it.")
    exit()

try:
    genai.configure(api_key=api_key)
    print("Generative AI configured successfully for project prjnanobanano (via API key)!")

    # --- Use the 'gemini-2.5-flash-image' model ---
    model = genai.GenerativeModel('gemini-2.5-flash-image') # Specify the correct model name

    print(f"\nUsing model: {model.name}")

    # --- Example 1: Pure text prompt (the model can still handle this) ---
    print("\n--- Example 1: Text-only prompt ---")
    text_prompt = "What is the capital of France?"
    text_response = model.generate_content(text_prompt)
    print(f"Text prompt: '{text_prompt}'")
    print(f"Model response: {text_response.text}")

    # --- Example 2: Text and Image prompt ---
    print("\n--- Example 2: Text and Image prompt ---")

    # IMPORTANT: You'll need an actual image file for this.
    # Replace 'path/to/your/image.jpg' with the actual path to an image on your system.
    # You can download a sample image or use one you have.
    # For example, create a file named 'banana.jpg' in the same directory as your script.
    image_path = 'banana.jpg' # Or 'path/to/your/image.png', etc.

    # Create a dummy image if you don't have one for testing
    if not os.path.exists(image_path):
        print(f"Creating a dummy image '{image_path}' for demonstration.")
        try:
            img = Image.new('RGB', (60, 30), color = 'yellow')
            img.save(image_path)
            print("Dummy image created. Please replace it with a real one for better results.")
        except ImportError:
            print("Pillow (PIL) library not found. Cannot create dummy image. Please install it: pip install Pillow")
            print("Or provide a real image file at:", image_path)
            exit()


    # Load the image
    img_data = Image.open(image_path)

    # Construct the multimodal content
    # The content is a list of parts. Each part can be text or an image.
    multimodal_content = [
        "What do you see in this image? Describe it.",
        img_data
    ]

    print(f"\nSending multimodal content to '{model.name}':")
    print(f"  - Text part: '{multimodal_content[0]}'")
    print(f"  - Image part: '{image_path}'")

    multimodal_response = model.generate_content(multimodal_content)

    print("\n--- Multimodal Model Response ---")
    print(multimodal_response.text)

except Exception as e:
    print(f"\nAn error occurred: {e}")
    print(f"Error type: {type(e)}")
    # Add more detailed error handling if needed