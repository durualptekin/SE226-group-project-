import os
import json
from google import genai
#i tried with gemini.generative... but new gemini library wants us to do it this way.to talk to the ai

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDZf03cHpFP3exTR_-nskUwOwUUe82GDdU")
#pulling


class GeminiService:
    def __init__(self, api_key=API_KEY):
        # The new SDK uses a centralized client initialized with your key
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"

    def generate_album_data(self, journal_text, genre, era, track_count):
        # the prompt for gemini """this area is used to add the prompt for the model, it helps with in long quotations"""
        prompt = f""" You are a professional music curator. Based on this journal entry, return ONLY valid JSON with this schema: 

        User wrote a journal entry: "{journal_text}"
        Desired Genre: {genre}
        Desired Era: {era}
        Number of Tracks: {track_count}

        Create a fictional album based on these details. The album should have a name, an artist, a release year, a label which are fully fictional. It also has a mood description in English, a detailed description of the album cover art (including colors, imagery, and style), and a list of relevant last.fm tags.
        Only return valid JSON with the following schema, dont add any extra text, only the JSON, and make sure it is valid JSON, if you cant create a album based on the details, return an empty JSON object {{
          "album_name": "Album name",
          "artist_name": "Artist name",
          "year": 2024,
          "label": "Label name",
          "mood_description": "Mood description in English",
          "cover_prompt": " A detailed description of the album cover art, including colors, imagery, and style",
          "lastfm_tags": ["tag1", "tag2"]  
        }}
        """
        # the prompt is a string that contains the instructions for the gemini model to generate text based on the
        # journal entry, genre, era, track count,
        # the prompt also includes instructions for the gemini model to return only valid JSON with a specific schema,
        # and to return an empty JSON object if it cannot create an album based on the details provided.
        # lastfm_tags is a list of tags that are relevant to the album,
        # it can be used to describe the genre, mood, or other characteristics of the album it stands for "last.fm tags"
        # which are tags that are used on the last.fm music platform to categorize and describe music.

        # for the answ
        try:
            # actually sending the huge prompt to the ai and waiting for it to reply
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)  # generate text from the gemini model using the prompt
            return self.parse_gemini_response(response.text)

        except Exception as e:  # if there is an error during the generation or parsing process, we catch the exception and print it, and return an empty JSON object
            print(f"Error generating album data: {e}")  # print the error message
            return self.parse_gemini_response("")

    def parse_gemini_response(self, response_text):
        # our plan b. if the ai if smt happens, we just show this default album so they wont see an error screen
        default_album = {
            "album_name": "Echoes of the Unknown",
            "artist_name": "The Enigma Project",
            "year": 2024,
            "label": "Independent Records",
            "mood_description": "A mysterious and undefined ambient atmosphere.",
            "cover_prompt": "An abstract, blurry, and mysterious landscape with muted colors.",
            "lastfm_tags": ["ambient", "experimental", "instrumental"]
        }

        if not response_text:
            return default_album

        clean_text = response_text.strip()

        # if ai said nothing, just use the backup
        if clean_text.startswith("```"):
            clean_text = clean_text.strip("`").strip()
            if clean_text.lower().startswith("json"):
                # remove the first 4 characters, which are "json"
                clean_text = clean_text[4:].strip()

        try:
            album_data = json.loads(clean_text)
            # parse the cleaned text into a Python dictionary using the json.loads method,
            # if the text is not valid JSON, it will raise a JSONDecodeError
            # which we catch in the except block below.

            # After parsing the JSON, we check if all the required keys are present in the album_data dictionary and
            # if they have valid values. If any key is missing or has an empty value, we print a warning message and
            # assign a default value from the default_album dictionary. This ensures that we always have a complete set of album data,
            # even if the Gemini model's response is incomplete or malformed.
            required_keys = [
                "album_name", "artist_name", "year", "label",
                "mood_description", "cover_prompt", "lastfm_tags"
            ]

            for key in required_keys:
                # checking if the ai forgot to give us some stuff
                # if it forgot one, we just take it from  default album
                if key not in album_data or not album_data[key]:
                    # If the key is missing or has an empty value, print a warning message and assign a default value from the default_album dictionary.
                    print(f"Warning: '{key}' is missing or empty in the Gemini response. Using default value:")
                    album_data[key] = default_album[key]

            raw_tags = album_data.get("lastfm_tags",[])
             # Get the raw tags from the album_data dictionary,
            # if the key "lastfm_tags" is not present, we use an empty list as a default value.
            optimized_tags = []
            # then iterate through the raw tags and clean them by converting them to lowercase,
            # stripping whitespace, and replacing spaces with hyphens.
            # check to ensure that the cleaned tag is not empty and not already in our optimized_tags list to avoid duplicates.
            # we limit the number of tags to a maximum of 6 as requested in task 4.
            # If all tags are invalid and removed, default tags from the default_album dictionary will be used

            # looping thru the tags to clean them up
            for tag in raw_tags:
                if isinstance(tag, str):
                    # convert to lowercase and replace spaces with hyphens
                    clean_tag = tag.lower().strip().replace(" ", "-")
                    # make sure it is not empty and not already in our list to avoid duplicates
                    if clean_tag and clean_tag not in optimized_tags:
                        optimized_tags.append(clean_tag)

            # limit the tags to max 6 elements as project doc says
            album_data["lastfm_tags"] = optimized_tags[:6]
            # fallback just in case all tags were somehow invalid and removed
            if not album_data["lastfm_tags"]:
                # if somehow all tags were problematic and the list is empty,
                # just use the default tags so last.fm does still work
                album_data["lastfm_tags"] = default_album["lastfm_tags"]


            return album_data  # return the album data as a Python dictionary,
            # if the JSON parsing is successful and all required keys are present with valid values,
            # we return the album_data dictionary.
            # If there was an error during JSON parsing or if any required keys were missing or empty,
            # we return the default_album dictionary instead.

        except json.JSONDecodeError as e:
            # If there is a JSON parsing error, we catch the exception and print an error message indicating that the model did not return valid JSON.
            print(f"JSON Parsing Error: {e}. Model did not return valid JSON. Using default album.")
            return default_album

        except Exception as e:
            print(f"Unexpected error occurred: {e}. Using default album.")
            # If any other unexpected error occurs during the parsing process, we catch the exception,
            return default_album
