import json
import logging

from django.conf import settings

import openai
import trafilatura
from pypdf import PdfReader

logger = logging.getLogger(__name__)

from infographs.infographs.exceptions import BlogContentNotFoundException


class URLAnalyzer:
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

