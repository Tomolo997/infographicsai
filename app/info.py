import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
from openai import OpenAI
import base64
from io import BytesIO
import os
from django.conf import settings
import markdown
import json

# Set up OpenAI API (you need to replace 'your-api-key' with your actual OpenAI API key)
openai_api_key = settings.OPENAI_API_KEY

def is_allowed(url, user_agent):
    rp = RobotFileParser()
    rp.set_url(urljoin(url, "/robots.txt"))
    rp.read()
    return rp.can_fetch(user_agent, url)

def is_disallowed_path(path):
    disallowed_paths = [
        "/trackback/",
        "/xmlrpc.php",
        "/wp-",
        "/cgi-bin/",
        "/wp-admin/"
    ]
    return any(path.startswith(p) or p in path for p in disallowed_paths)

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

def summarize_with_gpt(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes blog posts."},
            {"role": "user", "content": f"Summarize the following blog post into 4-8 main points with titles and short paragraphs:\n\n{text}"}
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog Post Summary</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: auto;
            line-height: 1.6;
        }
        h1, h2 {
            color: #333;
        }
        h1 {
            font-size: 2em;
            text-align: center;
        }
        h2 {
            font-size: 1.5em;
            margin-top: 1.5em;
        }
        p {
            margin-top: 0.5em;
        }
    </style>
</head>
<body>
<h1>{title}</h1>
"""

# URL of the blog post
url = "https://learnwirepro.com/docanalyzer-ai-review/"

# Check if scraping is allowed
user_agent = 'YourBot/1.0 (your@email.com)'
if not is_allowed(url, user_agent):
    print(f"Scraping not allowed for {url}")
else:
    # Check if the path is allowed
    path = urlparse(url).path
    if is_disallowed_path(path):
        print(f"Access to {path} is disallowed by robots.txt")
    else:
        # Fetch the content of the web page
        headers = {'User-Agent': user_agent}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all text content from the page
        full_text = soup.get_text(separator='\n', strip=True)

        # Summarize the content using GPT
        summary = summarize_with_gpt(full_text)
        # Convert markdown to HTML
        html_summary = markdown.markdown(summary)
        soup = BeautifulSoup(html_summary, 'html.parser')
        for tag in soup.find_all(['h3', 'p']):
            tag['contenteditable'] = 'true'
        html_summary = str(soup)
        
        html_content += html_summary

        html_content += """
        </body>
        </html>
        """

        # Save the HTML file
        html_file_path = 'blog_post_summary.html'
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print(f"Summary saved to {html_file_path}")

        # Convert HTML to JSON
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.find('h1').text

        sections = []
        for h3 in soup.find_all('h3'):
            section = {
                "title": h3.text,
                "content": h3.find_next('p').text if h3.find_next('p') else ""
            }
            sections.append(section)

        json_data = {
            "title": title,
            "sections": sections
        }

        # Convert to JSON string
        json_string = json.dumps(json_data, indent=2, ensure_ascii=False)

        # Save JSON to file
        json_file_path = 'blog_post_summary.json'
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json_file.write(json_string)

        print(f"JSON summary saved to {json_file_path}")