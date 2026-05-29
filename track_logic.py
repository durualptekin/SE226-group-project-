import random
from music_service import collect_tracks_from_tags


def remove_duplicate_tracks(track_list):
    """
    Removes duplicate songs from the list.
    if the same song (same name + same artist) appears from different tags,
    we only keep it once. comparison is case-insensitive so "hello" and "Hello" count as same.
    """
    seen = set()  # keeps track of which songs we already added
    unique_tracks = []

    for track in track_list:
        track_name = track.get("name", "").strip().lower()
        artist_info = track.get("artist", {})

        # last.fm returns artist as a dictionary like {"name": "Radiohead"}
        # but sometimes it might just be a string, so we handle both cases
        if isinstance(artist_info, dict):
            artist_name = artist_info.get("name", "").strip().lower()
        else:
            artist_name = str(artist_info).strip().lower()

        # we combine song name and artist as a tuple to create a unique identifier
        # so "Creep by Radiohead" wont appear twice even if it comes from both "sad" and "melancholic" tags
        identifier = (track_name, artist_name)

        if identifier not in seen and track_name != "":
            seen.add(identifier)
            unique_tracks.append(track)

    return unique_tracks


def select_final_tracklist(unique_tracks, desired_count, method="mixed"):
    """
    Picks the final tracks from our deduplicated pool.
    desired_count is what the user selected (between 6 and 14).
    
    method can be:
    - "popular" -> just takes the first N tracks (last.fm already sorts by popularity)
    - "random" -> picks randomly
    - "mixed" -> half popular half random, gives a nice balance
    """
    # if we dont have enough tracks just return whatever we have
    if len(unique_tracks) <= desired_count:
        return unique_tracks

    if method == "popular":
        return unique_tracks[:desired_count]

    elif method == "random":
        return random.sample(unique_tracks, desired_count)

    else:
        # mixed: take the top half by popularity, fill the rest randomly
        half = desired_count // 2
        popular_part = unique_tracks[:half]
        remaining = unique_tracks[half:]
        random_count = desired_count - half

        if len(remaining) >= random_count:
            random_part = random.sample(remaining, random_count)
        else:
            random_part = remaining

        return popular_part + random_part


def format_track_metadata(raw_track):
    """
    Takes a raw track dict from last.fm and extracts only the info we need:
    song name, artist name, and the last.fm url for the listen button.
    """
    song_name = raw_track.get("name", "Unknown Track")

    artist_info = raw_track.get("artist", {})
    if isinstance(artist_info, dict):
        artist_name = artist_info.get("name", "Unknown Artist")
    else:
        artist_name = str(artist_info) if artist_info else "Unknown Artist"

    # this url opens the song's page on last.fm when user clicks "Listen"
    track_url = raw_track.get("url", "")

    return {
        "name": song_name,
        "artist": artist_name,
        "url": track_url,
    }


def build_tracklist(tags, desired_count):
    """
    This is the main function that puts everything together.
    Called from main.py after Gemini gives us the tags.
    
    Steps:
    1- collect tracks from all tags via last.fm api
    2- remove duplicates (same song from different tags)
    3- select the right amount of tracks
    4- format them nicely for the UI
    """
    # step 1: get raw tracks from last.fm for each tag
    raw_tracks = collect_tracks_from_tags(tags, per_tag_limit=20)

    if not raw_tracks:
        print("No tracks found from Last.fm for the given tags.")
        return []

    # step 2: filter out duplicates
    unique_tracks = remove_duplicate_tracks(raw_tracks)

    if not unique_tracks:
        print("All tracks were duplicates somehow, this shouldnt happen normally.")
        return []

    # step 3: select final tracks based on desired count
    final_selection = select_final_tracklist(unique_tracks, desired_count, method="mixed")

    # step 4: clean up the data format for the UI to display
    formatted_tracklist = []
    for track in final_selection:
        formatted_tracklist.append(format_track_metadata(track))

    return formatted_tracklist
