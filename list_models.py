import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found.")
    exit()
client = genai.Client(api_key=API_KEY)

print("\nAvailable Gemini Models")
print("=" * 60)

try:
    models = client.models.list()

    for model in models:

        supported = getattr(
            model,
            "supported_actions",
            []
        )

        if "generateContent" in supported:

            print(f"Name: {model.name}")

            display_name = getattr(
                model,
                "display_name",
                ""
            )

            if display_name:
                print(
                    f"Display Name: {display_name}"
                )

            print(
                f"Supported: {supported}"
            )

            print("-" * 60)

except Exception as error:

    print("ERROR:")
    print(error)

