import json
import time
from openai import OpenAI
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# load dotenv variables
load_dotenv()


def extract_listings(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        listing = [(item['title'], item['description'], item['url']) for item in data]
        return listing


openAiClient = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
)

json_filename = 'job_listings.json'
listings = extract_listings(json_filename)

start_time = time.time()

jobPosition = "Android Developer"


def analyze_listing(client, title, description, url):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You help me find vacancies for "
                        f"{jobPosition}" +
                        ". Respond with 'yes' if the job is suitable, otherwise respond with 'no'. " +
                        "Answer is limited to 3 characters."},
            {"role": "user",
             "content": f"Is this job opening suitable for "+
                        f"{jobPosition}?\n\n{description}"}
        ],
        max_tokens=3
    )
    response = completion.choices[0].message.content.strip().lower()
    if response == 'yes':
        return f"{title} - {url}\n"
    return None


with open('results.txt', 'w', encoding='utf-8') as file, ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(analyze_listing, openAiClient, title, description, url) for title, description, url in
               listings]

    for future in as_completed(futures):
        result = future.result()
        if result:
            file.write(result)

end_time = time.time()
execution_time = end_time - start_time

minutes = int(execution_time // 60)
seconds = execution_time % 60

print(f"AI analysis was performed in {minutes} minutes and {seconds:.2f} seconds")