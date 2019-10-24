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
    message_list = msg.split("@")
    
    resp = MessagingResponse()

    if len(message_list) != 3:
        resp.message("Incorrect format.")
        return str(resp)
    
    if message_list[0] == "search":
        page = requests.get('https://www.linkedin.com/jobs/search/?keywords=' + message_list[1] + '&location=' + message_list[2])
        print(page)
        soup = BeautifulSoup(page.content, features="lxml")
        openings = soup.find_all("a", class_="result-card__full-card-link")
        if len(openings) > 5:
            openings = openings[:5]
        resp_message = ""
        for x in openings:
            temp = ""
            links = x["href"]
            openings_page = requests.get(links)
            openings_soup = BeautifulSoup(openings_page.content, features="lxml")
            job_title = openings_soup.find("h1", class_="topcard__title")
            if job_title:
                temp += "Job Title: " + job_title.text + "\n"
            job_location = openings_soup.find("span", class_="topcard__flavor topcard__flavor--bullet")
            if job_location:
                temp += "Location: " + job_location.text + "\n"
            company_title = openings_soup.find("a", class_="topcard__org-name-link")
            if company_title:
                temp += "Company: " + company_title.text + "\n"
            job_description = openings_soup.find("div", class_="description__text description__text--rich")
            if job_description:
                # temp += "Description:\n" + job_description.text + "\n"
                pass
            apply_link = openings_soup.find("a", class_="apply-button apply-button--link")
            if apply_link:
                apply_link = apply_link["href"]
                # temp += "Apply Link:\n" + apply_link + "\n"
            resp_message += temp + "\n"
            print(resp_message)
        resp.message(resp_message)
    else:
        resp.message("Other functions not implemented.")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)