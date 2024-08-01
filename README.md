# Preparing:

1. Download this project and open it with [PyCharm](https://www.jetbrains.com/pycharm/). Unpack the project and rename the file `.env_example` to `.env`.
2. Set your LinkedIn Username to `LINKEDIN_USERNAME` and LinkedIn Password to `LINKEDIN_PASSWORD`.
3. Open LinkedIn and upgrade your LinkedIn account to Premium.
4. Top up your [OpenAI account](https://platform.openai.com/) (minimum $5.00).
5. Go to [Dashboard ApiKeys](https://platform.openai.com/api-keys), create a new key, and add it to the `.env` file as the `OPENAI_API_KEY`.

# Installation:

1. Open the Terminal in your IDE and verify the Python installation with `python3 --version` (Linux, macOS) or `python --version` (Windows). If Python is not installed, you need to install Python 3.
2. Install the LinkedIn API library: `pip install git+https://github.com/tomquirk/linkedin-api.git`
3. Install the OpenAI Python library: `pip install --upgrade openai`
4. Install the DotEnv library for managing environment variables: `pip install python-dotenv`

# Patch the LinkedIn API Library to Add Search by Location Ability:

1. Open the file `LinkedIn_ConcurrentScraper.py` and locate the line with the text `result = api.search_jobs(`. 
   ![](./images/patch_linkedin_py_1.png)
2. Press and hold the `CTRL` key and click on `search_jobs`. This will take you to the file in the library directory:
   ![](./images/patch_linkedin_py_2.jpg)
3. In your file manager, replace the file `linkedin.py` with the updated file from this project.

# Before We Start:

1. Open `OpenAiTest.py` and run the file. You should see a `200 OK` response in the console after a request.
2. Log out of your LinkedIn account and log in again.

# Tuning:

To find jobs, you need to configure your location, search key, and the number of vacancies (limit) you want to retrieve (maximum 1000), as well as set GPT commands.

1. Find the location: Open the LinkedIn search page and perform a search, e.g., `React` `Poland`.
   ![](./images/jobs_search_1.png)
2. Set the location you found: Extract the `geoId` number from the URL and set it in `LinkedIn_ConcurrentScraper.py` in the `location_geo_id` field.
3. Set your search key, e.g., `React`, in `LinkedIn_ConcurrentScraper.py` in the `keywords` field.
4. Set your vacancies limit for searching, e.g., 5 (maximum 1000).
   ![](./images/jobs_search_2.png)
5. Configure GPT commands in the file `OpenAI_JobScreener.py`:

   5.1. System Role command context: Define the context that the system should know before your request. For example: `"Your role is a vacancy analyzer. Respond with 'yes' if the job is fully suitable for a React Developer; otherwise, respond with 'no'."`

   5.2. Request context: This will be sent with each vacancy in the User Role Content. For example: `f"Is this vacancy suitable for a React Software Developer? Yes or no?\n\n{description}"`

   5.3. Do not delete the literal `n` before the User Role Content; it is part of the system command as well.
   ![](./images/jobs_search_3.png)

# Running:

1. Open `LinkedIn_ConcurrentScraper.py` and run the script. After execution, you will get a `job_listings.json` file with the results.
2. Open `OpenAI_JobScreener.py` and run the script. After execution, you will get a `results.txt` file with the results. If it is empty, the robot could not select any jobs based on your request. Modify the context requests (5.1, 5.2) if necessary.
3. That's it! You're amazing!