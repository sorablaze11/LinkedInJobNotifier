from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    page = requests.get('https://www.linkedin.com/jobs/search/?keywords=intern&location=Bengaluru%2C%20Karnataka%2C%20India')
    soup = BeautifulSoup(page.content, features="lxml")
    openings = soup.find_all("a", class_="result-card__full-card-link")
    if len(openings) > 10:
        openings = openings[:10]

    for x in openings:
        links = x["href"]
        openings_page = requests.get(links)
        openings_soup = BeautifulSoup(openings_page.content, features="lxml")
        job_title = openings_soup.find("h1", class_="topcard__title").text
        job_location = openings_soup.find("span", class_="topcard__flavor topcard__flavor--bullet").text
        company_title = openings_soup.find("a", class_="topcard__org-name-link").text
        job_description = openings_soup.find("div", class_="description__text description__text--rich")
        print(job_title, ', ', company_title, ', ', job_location)
        apply_link = openings_soup.find("a", class_="apply-button apply-button--link")
        if apply_link:
            apply_link = apply_link["href"]
        print(apply_link)
        # print("Description:\n", job_description.text)
        print("--------------------------------------------------------------------------")
    
    # Create reply
    resp = MessagingResponse()
    resp.message("You said: {}".format(msg))

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)