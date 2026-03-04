import openai

ENDPOINT = "https://skt-hands-on-labs-001.openai.azure.com"
API_KEY = "E1Q4pO2gHbr25ZolTcS53MRRQlqr5N6t7ClcInF4HpdpHzLRiMMMJQQJ99CBACYeBjFXJ3w3AAABACOG0q1W"
API_TYPE = "azure"
API_VERSION = "2024-12-01-preview"

openai.azure_endpoint = ENDPOINT
openai.api_key = API_KEY
openai.api_type = API_TYPE
openai.api_version = API_VERSION

print("Welcome AI Poem!!")
print("-" * 100)

while True:
    subject = input("시의 주제를 입력하세요: ")
    if subject == "exit":
        break

    content = input("시의 내용을 입력하세요: ")

    result = openai.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role":"system","content":"너는 이제부터 인공지능 시인이야. 주제와 내용에 맞추어 감성적인 시를 써줘"},
                    {"role":"user","content":subject + "를 주제로 " + content + "를 내용으로 시를 지어줘"}
                ],
                temperature=1,
                max_tokens=500
    )

    print(result.choices[0].message.content)