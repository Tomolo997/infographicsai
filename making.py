import requests

# Icons for the "Philosophy and Legacy" infographic
icons = [
    {"prefix": "mdi", "name": "book", "description": "Meditations icon", "color": "blue"},
    {"prefix": "mdi", "name": "balance", "description": "Justice icon", "color": "green"}
]

icon_urls = []
for icon in icons:
    url = f"https://api.iconify.design/{icon['prefix']}:{icon['name']}.svg?color={icon['color']}&width=24&height=24"
    response = requests.get(url)
    if response.status_code == 200:
        icon_urls.append({"url": url, "description": icon["description"]})
    else:
        print(f"Failed to fetch {icon['name']} icon")

# Update JSON
infographic_json = {
    "metadata": {"title": "Marcus Aurelius: Stoic Wisdom", "contentType": "infographic"},
    "thematicAnalysis": {
        "mainTheme": "Philosophical Insight",
        "icons": icon_urls
    },
}
print(infographic_json)