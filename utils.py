


def sanitize_url(url):
    print("before sani-_>",url)
    if 'amp;' in url :
        url = url.replace("amp;","")
    while url.startswith("/"):
        url = url[1:]
    if url.startswith("www"):
        url = "https://"+url
    if url.startswith("http://"):
        url = "https://"+url[7:] 
    if not url.startswith("https://www.sardiniadigitallibrary.it/"):
        print(url)
    print("sanitized-->",url)

    return url