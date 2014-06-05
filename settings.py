SETTINGS = {
    "app_id": "deppo-svrd01",
    "site_domain": "clearfix-svr1.appspot.com",
    "site_name": "Deppo",
    "start_year": 2013,
    "enable_fb_login": True,
    "fb_id": "",
    "fb_secret": "",
    "fb_permissions": ["email"],
    "fb_app_access_token": "",
    "pubnub_subscriber_token": "",
    "pubnub_publisher_token": "",
    "pubnub_secret_key": "",
    "password_salt": "ENTER_SALT_HERE"  # Only set once. Do NOT change. If changed, users will not be able to login
}

SECRET_SETTINGS = {
    "fb_secret": "",
    "fb_app_access_token": "",
    "pubnub_secret_key": "",
    "server_base_url": "http://192.169.137.2:8080",
    "password_salt": "Pom64EaUrTAEjrsKqrhuAfNcW4U=LWdvZXM()ta$GVyZXIUCxIEV/#XNl.",  # Only set once. Do NOT change. If changed, users will not be able to login
    "mandrill_key": "pP2N91sc5E4IeD1vyy4jWQ"
}


SB_BOXES = {

    "sb_1": "medium",
    "sb_2": "medium",
    "sb_3": "small",
    "sb_4": "small",
    "sb_5": "xlarge",
    "sb_6": "medium",
    "sb_7": "small",
    "sb_8": "small",
    "sb_9": "large",
    "sb_10": "large",
}

DEPPO = {
    "small": [{"3": False}, {"4": False}, {"7": False}, {"8": False}],
    "medium": [{"1": False}, {"2": False}, {"6": False}],
    "large": [{"9": False}, {"10": False}],
    "xlarge": [{"5": False}]
}



RAYGUN_API_KEY = "mXYedKU7KmQutNNDWnHy8w=="

SAFEBOX_LOCATIONS = {

    "cebu" : [{"id":"SB01", "location":"it park", "address":"UP lahug"}]

}




# Local Settings
import os
def development():
    if os.environ['SERVER_SOFTWARE'].find('Development') == 0:
        return True
    else:
        return False


if development():
    SETTINGS["fb_id"] = "569550796388888"
    SECRET_SETTINGS["fb_secret"] = "be20b1c85858844bf561c82e139b25e8"
    SECRET_SETTINGS['fb_app_access_token'] = "539310509418887|dPefXXFnqaygLJ8RxWG_-9Xm9JY"