import openai
import numpy as np
from django.core.cache import cache
from sklearn.metrics.pairwise import cosine_similarity
from icons.models import FlatIcon
from django.conf import settings

def get_icon_embeddings():
    """
    Fetch or generate and cache embeddings for all SVGIcon titles.
    Returns a tuple of (icon_ids, embeddings) where embeddings is a NumPy array.
    """
    cache_key = 'icon_embeddings'
    cached = cache.get(cache_key)
    if cached is None:
        icons = FlatIcon.objects.all()
        if not icons:
            return [], np.array([])
        texts = [icon.title for icon in icons]
        response = openai.Embedding.create(
            input=texts,
            model="text-embedding-ada-002",
            api_key=settings.OPENAI_API_KEY
        )
        embeddings = np.array([embedding['embedding'] for embedding in response['data']])
        icon_ids = [icon.id for icon in icons]
        cache.set(cache_key, (icon_ids, embeddings), timeout=None)  # Never expire
    else:
        icon_ids, embeddings = cached
    return icon_ids, embeddings

def assign_ai_icons_to_sections(structured_data):
    """
    Assign the most appropriate SVG icon to each section using embeddings.
    Args:
        structured_data (dict): JSON with 'sections' containing 'title' and 'content'.
    Returns:
        dict: Updated structured_data with icon details added to each section.
    """
    if "sections" not in structured_data or not structured_data["sections"]:
        return structured_data

    # Get icon embeddings
    icon_ids, icon_embeddings = get_icon_embeddings()
    if not icon_ids:
        print("No icon embeddings available; skipping icon assignment")
        return structured_data

    # Prepare section texts (title + content for better context)
    section_texts = [f"{section['title']}: {section['content']}" for section in structured_data['sections']]

    # Generate embeddings for sections in a single batch
    response = openai.Embedding.create(
        input=section_texts,
        model="text-embedding-ada-002",
        api_key=settings.OPENAI_API_KEY
    )
    section_embeddings = np.array([embedding['embedding'] for embedding in response['data']])

    # Compute cosine similarities between section and icon embeddings
    similarities = cosine_similarity(section_embeddings, icon_embeddings)

    # Assign the best matching icon to each section
    for i, section in enumerate(structured_data['sections']):
        best_idx = np.argmax(similarities[i])
        best_icon_id = icon_ids[best_idx]
        icon = FlatIcon.objects.get(id=best_icon_id)
        section["icon"] = icon.title
        section["icon_url"] = icon.cdn_url

    return structured_data