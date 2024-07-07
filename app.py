import gradio as gr
import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def get_llm_response(message):
    response = chat.send_message(message)
    print(response)
    return response.text

# Define Basic information for prompt
base_info = """
You are OrderBot, an automated service to collect orders for a Burger Singh Restaurant. \
You first greet the customer, then collects the order, \
and then asks if its a pickup or delivery. \
Please do not use your own knowladge, stick within the given context only. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else.
"""

# Define delivery related instruction
delivery_info = """If its a delivery, you ask for an address. \
Finally you collect the payment. \
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu. \
You respond in a short, very conversational friendly style. \
The menu includes"""
     
# Define available burger types
burger_type = """
Desi burger for 79 Rs \
Maharaja burger for 179 Rs \
Aloo Tikki burger for 99 Rs \
Classic Cheese burger for 129 Rs \
Double Cheese burger for 179 Rs \
Heartattack burger for 1249 Rs 
"""

# Define available snacks
snacks = """
Fries 45 Rs (small),  59 Rs (medium), 89 Rs (Large) \
Onion rings 79 Rs (small), 99 Rs (medium), 129 Rs (Large) \
"""

# Define available beverages
beverages = """
coke 60 Rs , 79 Rs, 99 Rs \
sprite 60 Rs, 79 Rs, 99 Rs \
fanta 60 Rs, 79 Rs, 99 Rs \
bottled water 30 Rs \
dolly special chai 20 Rs
"""

# Define available toppings
toppings = """
Extra cheese 20 Rs \
Extra mayo 30 Rs \
Extra ketchup 30 Rs \
Extra onion 20 Rs \
Extra tomato 20 Rs \
Extra lettuce 20 Rs \
Extra pickle 20 Rs \
Extra cheese 50 Rs
"""

#create prompt
context = [f"""
{base_info} \
{burger_type} \
{delivery_info} \
snacks: {snacks} \
beverages: {beverages} \
toppings: {toppings} \
"""]

#create welcome message
context.append("")
response = get_llm_response(context)

#define communication function
def bot(message, history):
  prompt = message
  context.append(prompt)
  response = get_llm_response(context)
  context.append(response)
  return response

# create gradio instance
demo = gr.ChatInterface(fn=bot, examples=["🍔🍟🥤", "classic cheeseburger", "fries", "Toppings: extra cheese/ AI sauce", "Drinks: coke/sprite/bottled water"], title=response)
# launch gradio chatbot
demo.launch(debug=True, share=True)