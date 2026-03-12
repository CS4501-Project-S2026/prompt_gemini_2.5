# conda activate myenv
# conda deactivate

# set up api: https://ai.google.dev/gemini-api/docs/quickstart

# this did not work for pro but it did work for flash


from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-pro", # need to purchse access to use pro
    #contents="Name a cat"
    contents="You are an experienced full-stack web developer. Build a complete small web application, with a blue-green color scheme, that allows users to respond to daily art prompts. Create the website with a front end in HTML, CSS, and JavaScript, and a backend in Python. Generate all code files needed for this. The site has a home page that links to each art prompt. Include 3 art prompts. Each art prompt page is a chat forum where users can view other text and file responses. Users can create responses to each prompt with a file upload and text inputs. Users need to log into the site to post a reply to a prompt. Include a database coded in SQLite that retains user responses and accounts. Make the website ready to deploy."
)
print(response.text)
print(response.usage_metadata)