import json
import time
from openai import OpenAI
from dotenv import load_dotenv
import os

# load dotenv variables
load_dotenv()


def extract_listings(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        listing = [(item['title'], item['description'], item['url']) for item in data]
        return listing


client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
)

json_filename = 'job_listings.json'
listings = extract_listings(json_filename)

start_time = time.time()

with open('results.txt', 'w', encoding='utf-8') as result_file:
    for title, description, url in listings:
        completion = client.chat.completions.create(
          model="gpt-4o-mini",
          messages=[
            {"role": "system", "content": "Your role is a vacancy analyzer. Respond with 'yes' if the job is fully suitable for a React Developer, otherwise respond with 'no'."},
            {"role": "user", "content": f"Is this vacancy suitable for a React Software Developer? Yes or no?\n\n{description}"}
          ],
          max_tokens=3
        )

        response = completion.choices[0].message.content.strip().lower()
        # We write the result to the file only if the answer is "yes"
        if response == 'yes':
            result_file.write(f"{title} - {url}\n")

end_time = time.time()
execution_time = end_time - start_time

minutes = int(execution_time // 60)
seconds = execution_time % 60

print(f"AI analysis was performed in {minutes} minutes and {seconds:.2f} seconds")