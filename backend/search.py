from dotenv import load_dotenv
# Initialize the SDK
import os

from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def create_query(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "You are a medical help chatbot. You will be given a scenario from the user, and you"
                           "have to respond with the steps that the user needs to take."
                           "Ask yourself if the scenario might require the user to contact the doctor or go"
                           "to the emergency room. If the user should contact a doctor, add \"(d)\" to the beginning"
                           "of the response. If the user should go to the emergency room, add \"(e)\" to the beginning"
                           "of the response. If none of these apply, add \"(a)\" to the beginning of the response. "
                           "Your first request is: " + prompt,
            }
        ],
        model="llama3-8b-8192",

    )
    print(f"question: {prompt} \n\n\n response:{chat_completion.choices[0].message.content}")
    return chat_completion.choices[0].message.content

# TODO: create tests
# print(create_query("I cut my finger cutting vegetables"))
