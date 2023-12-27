import openai
import json
import os
import uuid
from config import OPENAI_KEY

class GPTAssistant:
    def __init__(self, session_id=None):
        self.client = openai.OpenAI(api_key=OPENAI_KEY)
        if session_id is None:
            self.generate_unique_session_id()
            self.conversation_history = []
        else:
            self.session_id = session_id
            self.retrieve_conversation_from_file()

    def gpt_response(self, user_message):
        # Create a list of messages with the user's input and previous assistant responses
        self.conversation_history.append({"role": "user", "content": user_message})
        messages = [
            {"role": "system", "content": "You are a helpful assistant."}] + self.conversation_history

        # Call the OpenAI API to generate a response asynchronously
        response = self.client.chat.completions.create(
            model='gpt-4',
            messages=messages
        )
        # Extract the assistant's reply (converted to a string)
        assistant_reply = str(response.choices[0].message.content)
        self.conversation_history.append({"role": "assistant", "content": assistant_reply})
        # Save conversation history to a file with session_id
        self.save_conversation_to_file()

        return assistant_reply

    def generate_unique_session_id(self):
        self.session_id = str(uuid.uuid4())

    def save_conversation_to_file(self):
        # Check if the directory exists, create it if not
        if not os.path.exists("conversation_history"):
            os.makedirs("conversation_history")

        filename = f"conversation_{self.session_id}.json"
        filepath = os.path.join("conversation_history", filename)

        with open(filepath, "w") as file:
            json.dump(self.conversation_history, file)

    def retrieve_conversation_from_file(self):
        filename = f"conversation_{self.session_id}.json"
        filepath = os.path.join("conversation_history", filename)

        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                conversation = json.load(file)
                self.conversation_history = conversation  # Update conversation_history
                return conversation
        else:
            self.conversation_history = [] 
            return []

if __name__== "__main__":
    # Example usage:
    assistant = GPTAssistant()
    # Send the initial message
    user_message_1 = "Tell me a joke."
    print(user_message_1)
    response_1 = assistant.gpt_response(user_message_1)
    session_id = assistant.session_id
    print("Assistant's response 1:", response_1)

    # Create a new assistant object and continue the conversation
    new_assistant = GPTAssistant(session_id)

    user_message_2 = "Tell me a second joke related to your first joke."
    print(user_message_2)
    print(f"convos_hist {new_assistant.conversation_history}")
    response_2 = new_assistant.gpt_response(user_message_2)
    print("Assistant's response 2:", response_2)