import requests

def get_books(user_id: int, shelf: str = "read"):
    # shelf can be "read", "currently-reading", "want-to-read"
    # Fetches all pages and returns a single merged response
    all_books = []
    page = 1
    per_page = 100

    while True:
        url = f"https://api.piratereads.com/{user_id}/{shelf}?per_page={per_page}&page={page}"
        response = requests.get(url)
        if not response.ok or not response.text.strip().startswith("{"):
            break
        books = response.json().get("books", [])
        if not books:
            break
        all_books.extend(books)
        page += 1

    return {"books": all_books, "count": len(all_books)}

def get_all_books(user_id: int):
    read = get_books(user_id, "read")
    reading = get_books(user_id, "currently-reading")
    want_to_read = get_books(user_id, "want-to-read")
    return {"read": read, "currently_reading": reading, "want_to_read": want_to_read}