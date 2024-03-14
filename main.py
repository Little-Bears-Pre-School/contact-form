import os

import functions_framework
import httpx
from flask import redirect


@functions_framework.http
def contact_form(request):
    # only bots will fill in this honeypot field
    if request.form.get("middle_name"):
        return redirect("https://little-bears.com/contact-success", code=302)

    sender_email = request.form["email"]
    sender_name = f"{request.form['first_name']} {request.form['last_name']}"
    body = request.form["message"]

    httpx.post(
        f'https://api.mailgun.net/v3/{os.getenv("MAILGUN_DOMAIN_NAME")}/messages',
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={
            "from": f"{sender_name} <{sender_email}>",
            "to": "hello@little-bears.com",
            "subject": "Website Contact Form Submission",
            "text": f'{body}\n\nTel: {request.form["phone"]}',
        },
    )

    return redirect("https://little-bears.com/contact-success", code=302)