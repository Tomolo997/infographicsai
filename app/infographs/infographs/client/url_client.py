import base64
import json
import logging
from io import BytesIO

from django.conf import settings

import openai
import trafilatura
from PIL import Image
from pypdf import PdfReader

logger = logging.getLogger(__name__)

from infographs.infographs.exceptions import BlogContentNotFoundException


class URLAnalyzer:
    def _analyze_template_image(self, image_file):
        """Analyze template image using GPT-4 Vision and extract design schema"""
        logger.info("Starting template image analysis with GPT-4 Vision")
        
        try:
            # Read and encode the image
            if hasattr(image_file, 'read'):
                image_data = image_file.read()
                image_file.seek(0)  # Reset file pointer
            else:
                with open(image_file, 'rb') as f:
                    image_data = f.read()
            
            # Encode image to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            logger.debug("Image encoded to base64")
            
            # Initialize OpenAI client
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            
            prompt = """Analyze this infographic template and describe its visual structure. I need you to identify:

The overall layout pattern - how is the content organized? Is it a grid, vertical sections, or something else?

Color scheme - what are the primary colors used and how are they distributed across the design?

Component structure - break down the major sections (header, body, footer) and describe what elements each contains

Typography - what text hierarchy exists (titles, subtitles, labels)?

Icon usage - where are icons placed, what size, what color?

Spacing and alignment - how are elements positioned relative to each other?

Any borders, shadows, or decorative elements

The goal is to extract the design system and layout rules so I can recreate similar templates programmatically. Focus on the structural and visual properties, not the actual content.
"""
            
            logger.debug("Sending request to GPT-4 Vision")
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in analyzing visual designs and extracting design specifications. You excel at identifying colors, layouts, typography, and visual patterns."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            # Get the text description
            template_description = response.choices[0].message.content
            
            if not template_description or template_description.strip() == "":
                raise ValueError("Empty response from GPT-4 Vision")
            
            logger.info("Successfully analyzed template image with GPT-4 Vision")
            logger.debug(f"Template description: {template_description[:200]}...")
            
            # Return as a simple dict with the description
            template_design = {
                "template": {
                    "description": template_description
                }
            }
            logger.info("Successfully analyzed template image with GPT-4 Vision")
            logger.debug(f"Template schema: {json.dumps(template_design, indent=2)}")
            
            return template_design
            
        except Exception as e:
            logger.error(f"Error analyzing template image: {str(e)}", exc_info=True)
            # Return a default schema if analysis fails
            return {
                "template": {
                    "body": {
                        "layout": "grid",
                        "textColor": "#000000",
                        "colors": ["#2ECC71", "#F39C6B", "#5DADE2"]
                    }
                }
            }
    
    def _read_pdf(self, pdf_file):
        """Helper method to read PDF content"""
        logger.info("Starting to read PDF file")

        try:
            # Read the PDF file
            pdf_reader = PdfReader(pdf_file)
            
            # Extract text from all pages
            text_content = []
            for page_num, page in enumerate(pdf_reader.pages, start=1):
                logger.debug(f"Extracting text from page {page_num}")
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
            
            # Combine all pages
            full_text = "\n\n".join(text_content)
            
            if not full_text.strip():
                logger.error("Could not extract text from PDF")
                raise BlogContentNotFoundException(
                    "Could not extract text from this PDF. The PDF might be empty, image-based, or protected."
                )
            
            logger.info(f"Successfully extracted text from PDF. Total length: {len(full_text)}")
            
            result = {
                "title": "PDF Document",
                "meta_description": "",
                "content": full_text,
            }
            return result
            
        except BlogContentNotFoundException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error while reading PDF: {str(e)}", exc_info=True)
            raise BlogContentNotFoundException(
                f"An error occurred while trying to read this PDF: {str(e)}"
            )

    def _scrape_website(self, url):
        """Helper method to scrape website content using trafilatura"""
        logger.info(f"Starting to scrape website: {url}")

        try:
            logger.debug(f"Fetching URL: {url}")
            # Fetch the webpage
            downloaded = trafilatura.fetch_url(url)
            
            if not downloaded:
                logger.error(f"Failed to fetch content from {url}")
                raise BlogContentNotFoundException("Could not fetch content from this webpage. The page might be empty or require JavaScript to load content.")

            logger.debug("Successfully fetched webpage, extracting content")

            # Extract main content (excluding comments)
            content = trafilatura.extract(downloaded, include_comments=False)
            
            # Extract metadata
            metadata = trafilatura.extract_metadata(downloaded)

            if not content:
                logger.error("Could not extract content from the page")
                return {
                    "title": "Content Not Found",
                    "meta_description": "",
                    "content": "Could not extract content from this webpage. The page might be empty or require JavaScript to load content.",
                }

            # Get title from metadata or fallback
            title = ""
            if metadata and metadata.title:
                title = metadata.title
            elif metadata and metadata.sitename:
                title = metadata.sitename

            # Get meta description from metadata
            meta_desc = ""
            if metadata and metadata.description:
                meta_desc = metadata.description

            # Clean up content - remove extra whitespace and empty lines
            text = content

            logger.debug(f"Extracted text length: {len(text)}")

            result = {
                "title": title[:200] if title else "",  # Limit title length
                "meta_description": meta_desc[:500] if meta_desc else "",  # Limit description length
                "content": text
                ,  # Limit content length
            }
            logger.info(f"Successfully scraped website. Content length: {len(text)}")
            return result

        except Exception as e:
            logger.error(
                f"Unexpected error while scraping {url}: {str(e)}", exc_info=True
            )
            return {
                "title": "Error",
                "meta_description": "",
                "content": "An error occurred while trying to extract content from this webpage.",
            }

    def _analyze_with_gpt(self, website_data, language="English"):
        """Helper method to analyze website content with GPT and return structured JSON with icon suggestions"""
        logger.info(
            "Starting GPT website analysis for JSON structure with icon suggestions"
        )

        try:
            logger.debug("Initializing OpenAI client")
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

            # Updated schema to include icon_keywords field
            infographic_schema = {
                "name": "infographic_content",
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Main title for the infographic",
                            "maxLength": 200,
                        },
                        "subTitle": {
                            "type": "string",
                            "description": "Subtitle or brief description for the infographic",
                            "maxLength": 200,
                        },
                        "summary": {
                            "type": "string",
                            "description": "Summary of the infographic",
                            "maxLength": 1000,
                        },
                    },
                    "required": ["title", "subTitle", "summary"],
                    "additionalProperties": False,
                },
                "strict": True,
            }

            prompt = f"""
            Analyze this website content and extract key information for an infographic:
            
            Title: {website_data['title']}
            Meta Description: {website_data['meta_description']}
            
            Content:
            {website_data['content']}
            
            Structure the information for an infographic with:
           
            IMPORTANT: The content must be in the {language} language of the content.
            """

            logger.debug(
                f"Sending request to GPT. Content length: {len(website_data['content'])}"
            )

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an infographic content specialist. Extract and structure key information from websites and suggest appropriate visual elements.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": infographic_schema,
                },
                max_tokens=1000,
                temperature=0.5,
            )

            analysis_json = json.loads(response.choices[0].message.content)
            logger.info(
                "Successfully received structured JSON from GPT with icon suggestions"
            )
            logger.debug(f"JSON preview: {str(analysis_json)[:200]}...")

            return analysis_json
        except Exception as e:
            logger.error(f"Error in GPT analysis: {str(e)}", exc_info=True)
            pass

