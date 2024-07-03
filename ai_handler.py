from typing import Dict, List
from openai import OpenAI

from handler import SearchQuery, run_query
from logger import logging


def text_handler(messages: List[Dict[str, str]]):
    user_text = messages[0]["content"]
    prompt = (
        f'Given text: "{user_text}". '
        "You offer Tech Recruiter services and are helping your client find engineers. "
        "Your task is to extract employment type, budget, and skills from the user text. "
        "All your responses should be conversational, addressing the client directly "
        "until you obtain all three pieces of information. "
        "If the employment type (full time or part time) is not mentioned, ask the user which one they are looking for. "
        "A valid budget is a number on a per month basis, for example, 2000 or 10000. "
        "If the budget is not provided, ask the user for it. "
        "Valid skills are a list of comma-separated strings, for example, python, java, c++. "
        "If the skills are not provided in the text, reply by asking the user for them. "
        "Once you have obtained all three pieces of information, "
        "reply only in the format below and no other words: "
        "Search Query: {employmenttype}|{budget}|{skills}"
        "Example: employmenttype: fulltime or parttime"
        "Example: budget: 2000, must be a number only, no extra words or characters."
        "Example: skills: python,java,c++"
    )

    messages[0]["content"] = prompt
    if messages[0]["role"] != "system":
        messages.insert(
            0, {"role": "system", "content": "You are a helpful assistant."}
        )
    messages = ai_conversations(messages)

    if "Search Query:" in messages[-1]["content"]:
        for line in messages[-1]["content"].split("\n"):
            if "search query:" in line.lower():
                logging.info(f"Search Query: {line.split(':')[1].strip()}")
                search_query = line.split(":")[1].strip()
                search_query = SearchQuery(
                    is_full_time="full" in search_query.lower(),
                    is_part_time="part" in search_query.lower(),
                    full_time_salary="".join(
                        filter(str.isdigit, search_query.split("|")[1])
                    ),
                    part_time_salary="".join(
                        filter(str.isdigit, search_query.split("|")[1])
                    ),
                    skills=[
                        skill.strip().lower()
                        for skill in search_query.split("|")[2].split(",")
                    ],
                )
                search_results = run_query(search_query)
                if search_results:
                    messages.append(
                        {
                            "role": "system",
                            "content": "Here are the top candidates matching your search query:\n\n",
                        }
                    )
                    for i, result in enumerate(search_results):
                        messages[-1]["content"] += (
                            f"{i+1}: {result['name']} - {result['email']} - {result['phone']}\n"
                            f"{'Full Time' if search_query.is_full_time else 'Part Time'}Salary: "
                            f"{result['fullTimeSalary'] if search_query.is_full_time else result['partTimeSalary']} per month\n\n"
                        )
                else:
                    messages.append(
                        {
                            "role": "system",
                            "content": "No candidates found matching your search query.",
                        }
                    )
                break

    return messages


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
