import requests

#last.fm api base url - all requests go to this single endpoint
LASTFM_BASE_URL = "https://ws.audioscrobbler.com/2.0/"
LASTFM_API_KEY = "5b6b8422007751999e063079e07c67e7"


def fetch_tracks_by_tag(tag, limit=20):
    """Fetches top tracks for a given tag from the Last.fm API using tag.gettoptracks."""
    
    # setting up the parameters for the API request
    params = {
        "method": "tag.gettoptracks",
        "tag": tag,
        "limit": limit,
        "api_key": LASTFM_API_KEY,
        "format": "json",
    }
    # user agent header is required by last.fm, otherwise they might block us
    headers = {"User-Agent": "PDA226-AlbumCoverStudio/1.0"}

    try:
        response = requests.get(LASTFM_BASE_URL, params=params,
                                headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        # the json structure from last.fm is: {"tracks": {"track": [...]}}
        # so we need to dig into it to get the actual list
        tracks = data.get("tracks", {}).get("track", [])
        return tracks

    except requests.exceptions.Timeout:
        print(f"Timeout while fetching tag: {tag}")
        return []
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error for tag '{tag}': {http_err}")
        return []
    except requests.exceptions.RequestException as req_err:
        # this catches any other connection problems (no internet etc)
        print(f"Connection error for tag '{tag}': {req_err}")
        return []
    except ValueError:
        # this happens if the response is not valid json for some reason
        print(f"Could not parse JSON response for tag: {tag}")
        return []


def collect_tracks_from_tags(tag_list, per_tag_limit=20):
    """
    Goes through each tag one by one and collects all the tracks.
    We get around 20 tracks per tag, so with 4-6 tags we end up with 80-120 raw tracks
    before removing duplicates.
    """
    all_tracks = []

    for tag in tag_list:
        # fetch tracks for this specific tag
        results = fetch_tracks_by_tag(tag, limit=per_tag_limit)
        all_tracks.extend(results)
        # we just add them all together, duplicates will be handled in track_logic.py

    return all_tracks
