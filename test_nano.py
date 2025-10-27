# import google.generativeai as genai
# import os

# # Replace with your actual API key
# api_key = "AIzaSyB-KiR83uGM7z_P7RdFbVinn7Wsi7VzRVw"

# try:
#     client = genai.Client(api_key=api_key)
#     print("Client initialized successfully!")
#     # If successful, you can try a simple model call
#     # model = client.get_model("gemini-pro")
#     # print(f"Model: {model.name}")
# except Exception as e:
#     print(f"Error initializing client: {e}")
#     print(f"Error type: {type(e)}")
#     print(f"Current working directory: {os.getcwd()}")
#     print(f"User home directory: {os.path.expanduser('~')}")


import google.generativeai as genai
import os

# It's best practice to load API keys securely, e.g., from environment variables
# For testing, you can hardcode it here, but avoid in production
# api_key = os.getenv("GOOGLE_API_KEY") # Or directly "YOUR_API_KEY_HERE" if testing
api_key = "AIzaSyB-KiR83uGM7z_P7RdFbVinn7Wsi7VzRVw"

if not api_key:
    print("API Key not found. Please set the GOOGLE_API_KEY environment variable or hardcode it.")
    exit()

try:
    # Configure the genai library with your API key
    genai.configure(api_key=api_key)
    print("Generative AI configured successfully!")

    # Now you can interact with models
    # For example, to list available models:
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(f"  {m.name}")

    # To get a specific model and make a request (example):
    # model = genai.GenerativeModel('gemini-pro')
    # response = model.generate_content("Tell me a story about a magical banana.")
    # print("\nStory from the model:")
    # print(response.text)

except Exception as e:
    print(f"Error configuring Generative AI: {e}")
    print(f"Error type: {type(e)}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"User home directory: {os.path.expanduser('~')}")