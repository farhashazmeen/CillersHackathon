import strawberry
import logging
import openai
from .. import types
from ..auth import IsAuthenticated


logger = logging.getLogger(__name__)

#Configure your OpenAI API key (ensure it's securely stored in your environment variables)
openai.api_key = "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"

@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def getopenai(self, prompt: str) -> types.Message:
        try:
            # Using the correct ChatCompletion API
            response = openai.chat.completions.create(
                model="gpt-4",  # Use "gpt-3.5-turbo" if you don't have access to GPT-4
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=50  # Adjust this as needed
            )

            # Extract the generated response from the choices
            #generated_text = response['choices'][0]['message']['content'].strip()
            message_content = response.choices[0].message.content
            # Return the response to the user
            return types.Message(message=message_content)

        except Exception as e:
            logger.error(f"Error querying OpenAI: {e}")
            return types.Message(message="An error occurred while processing your request.")
