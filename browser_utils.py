import webbrowser

def open_music_link(url):
    """Opens the given url link on the browser of the user."""
    print(f"Opening browser: {url}")
    webbrowser.open(url)

"""Testing part, delete it later!"""
if __name__ == "__main__":
    test_link = "https://www.last.fm"
    open_music_link(test_link)