from google.appengine.api import urlfetch
import json

base_url = "https://rest.nexmo.com/sms/json"

api_key = "1c22cbce"
api_secret = "7695677d"

def send_sms(to, code, kind):
	if kind == "receiver":
		text = "Hi, Happy Valentines Day, Someone give you a gift!., go to this address (UP lahug, Near Gate 2 in the covered walk) Please use this pin to open the box(" + " " + code + " " +") - powered by: DEPPO"
	elif kind == "sender":
		text = "The Package has been claimed, thank you for using Deppo!."

	payload = {"api_key": api_key, "api_secret": api_secret}
	payload['from'] = "deppo.co"
	payload['to'] = to
	payload['text'] = text.strip()
	response = urlfetch.fetch(url=base_url, method=urlfetch.POST, payload=json.dumps(payload), headers={"Content-Type": "application/json"}).content

	return response