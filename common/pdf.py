import requests


def html_to_pdf(html):
    response = requests.post(
        "http://gotenberg:3000/forms/chromium/convert/html",
        files={"file": ("index.html", html)},
        data={"preferCssPageSize": "true"},
    )
    return response.content
