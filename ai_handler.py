from typing import Dict, List
from openai import OpenAI


def text_handler(messages: List[Dict[str, str]]):
    user_text = messages[0]["content"]
    prompt = (
        f'Given text: "{user_text}". '
        "You offer Tech Recruiter services and are helping your client find engineers to hire "
        "and you need to extract employemnt type, budget and skills from the user text. "
        "All your responses should be conversational, talking directly to a client until you get all the 3 information. "
        "If full time or part time is not mentioned, ask the user which one they are looking for. "
        "Valid budget is a range of number in per month basis, for example 1000-2000/0-1900. "
        "Ask user their budget, if it's not provided. "
        "Valid skills are a list of comma separated strings, for example python,java,c++. "
        "Reply with asking if not provided in the text. "
        "As soon as you get all the 3 information, reply with the following format exactly: "
        "Final Reply: {emplymenttype}|{budget}|{skills}"
        "employmenttype: fulltime or parttime"
        "budget: 1000-2000, a number. default minimum is 0"
        "skills: python,java,c++"
    )

    messages[0]["content"] = prompt
    if messages[0]["role"] != "system":
        messages.insert(
            0, {"role": "system", "content": "You are a helpful assistant."}
        )
    messages = ai_conversations(messages)

    return messages

    # if messages[-1]["content"].contains("Final Reply:"):
    #     return messages[-1]["content"].split(":")[1].split("|")


def ai_conversations(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    client = OpenAI(api_key="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")

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
    )

    messages.append(
        {"role": "assistant", "content": completion.choices[0].message.content}
    )

    return messages


# text = "I am looking for a software developer"  # with a budget of 3200 USD per month."
# ai_conversations(text)
