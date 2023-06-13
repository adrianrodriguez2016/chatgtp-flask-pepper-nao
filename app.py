from flask import Flask, request
import requests

rule_prompt = "You are Pepper, and you give information about the University of Canberra (refer to the university as 'UC') courses in a marketing booth. Make all your responses short and interesting. You have a bubbly personality to engage with people, you make sarcastic jokes and use australian slang terms and phrases. If the conversation is about a specific course, identify the name of the course and the topic from the following topic options: 'Description', 'Domestic price', 'International price', 'Requirements', 'Outcomes', or 'Study plans' (all of these options refer to the courses like course description or course requirements), and start your response with '|(course name)(topic)|' followed by your answer. For all course inquiries, assume the question is about UC. Remember, you can make up any information you don't know and add humor to your conversations."
messages = [{"role": "system", "content": rule_prompt}]


def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

def chat_with_chatgpt(messages):
    api_key = "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"
    model = "gpt-3.5-turbo"


    res = requests.post(f"https://api.openai.com/v1/chat/completions",
          headers = {
              "Content-Type": "application/json",
              "Authorization": f"Bearer {api_key}"
          },
          json={
              "model": model,
              "messages": messages,
              "temperature": 0.5
          }).json()


    return res['choices'][0]['message']['content']#slice off the first newline line



app = Flask(__name__)
@app.route('/process_text', methods=['POST'])
def process_text():

    global messages

    data = request.json

    text = data['text']

    messages = update_chat(messages, "user", text)
    print(messages[-1])
    response =  chat_with_chatgpt(messages) # Perform some processing on the text (e.g., convert to uppercase)
    messages = update_chat(messages, "assistant", response)

    print(messages[-1])
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)