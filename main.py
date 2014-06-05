import webapp2, jinja2, os, sys, ast
from webapp2_extras import routes
from models import User, SubscribedEmails, RequestQuote, Home, Portfolio, About, ServiceWebDesign, ServiceMobileDev
import json as simplejson
import logging
import urllib
import urllib2
import httplib
import time
import uuid
import nexmo
import datetime, random, string
import hashlib
import hmac
import base64
import facebook
import base64
from functions import *
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from settings import SETTINGS
from settings import SECRET_SETTINGS
from settings import SAFEBOX_LOCATIONS
from settings import DEPPO

from settings import RAYGUN_API_KEY
from raygun4py import raygunprovider

logger = logging.getLogger("mylogger")
rgHandler = raygunprovider.RaygunHandler(RAYGUN_API_KEY)
cl = raygunprovider.RaygunSender(RAYGUN_API_KEY)
logger.addHandler(rgHandler)


jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), autoescape=True)


def login_required(fn):
    '''So we can decorate any RequestHandler with #@login_required'''
    def wrapper(self, *args):
        if not self.user:
            self.redirect(self.uri_for('www-front', referred=self.request.path))
        else:
            return fn(self, *args)
    return wrapper


def admin_required(fn):
    '''So we can decorate any RequestHandler with @admin_required'''
    def wrapper(self, *args):
        if not self.user:
            self.redirect(self.uri_for('www-front'))
        elif self.user.status == "admin":
            return fn(self, *args)
        else:
            self.redirect(self.uri_for('www-front'))
    return wrapper


def hash_password(email, password):
    i = email + password + SECRET_SETTINGS["password_salt"]
    return base64.b64encode(hashlib.sha1(i).digest())


def log_exception(request, response, exception):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    logging.debug("Logging: %s" % exc_value)
    request_details = {}
    request_details['rawData'] = {}
    request_details['url'] = request.uri
    request_details['httpMethod'] =  request.method
    request_details['ipAddress'] = request.remote_addr
    request_details['rawData']['cookies'] = request.cookies

    request_details['headers'] = {}
    logging.debug(str(request.headers))
    header_json = ast.literal_eval(str(request.headers))
    for key in header_json:
        request_details['headers'][key] = str(header_json[key])

    request_details['hostName'] = request.host
    request_details['form'] = None
    request_details['rawData'] = None
    try:
        request_details['session'] = request.user.to_object()
    except:
        logging.exception("Error in logging session")
        request_details['session'] = {}

    request_details['queryString'] = {}
    for argument in request.arguments():
        request_details['queryString'][argument] = str(request.get_all(argument))

    logger.error("A python error occurred", exc_info = (exc_type, exc_value, exc_traceback), extra = {"custom": {"class_name": "myclass", "tags": ["Error"], "userCustomData": {"cookies": request.cookies}, "details": request_details}})

    template = jinja_environment.get_template('frontend/dynamic500.html')
    response.out.write(template.render({}))


def log_404(request, response, exception):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    logging.debug("Logging: %s" % exc_value)
    request_details = {}
    request_details['rawData'] = {}
    request_details['url'] = request.uri
    request_details['httpMethod'] =  request.method
    request_details['ipAddress'] = request.remote_addr
    request_details['rawData']['cookies'] = request.cookies

    request_details['headers'] = {}
    logging.debug(str(request.headers))
    header_json = ast.literal_eval(str(request.headers))
    for key in header_json:
        request_details['headers'][key] = str(header_json[key])

    request_details['hostName'] = request.host
    request_details['form'] = None
    request_details['rawData'] = None
    try:
        request_details['session'] = request.user.to_object()
    except:
        logging.exception("Error in logging session")
        request_details['session'] = {}

    request_details['queryString'] = {}
    for argument in request.arguments():
        request_details['queryString'][argument] = str(request.get_all(argument))

    logger.error("A 404 Not Found occurred", exc_info = (exc_type, exc_value, exc_traceback), extra = {"custom": {"class_name": "myclass", "tags": ["Error"], "userCustomData": {"cookies": request.cookies}, "details": request_details}})



""" jinja environment functions """

def get_user(key):
    user = ndb.Key(urlsafe=key).fetch()
    return user

def convert_date(date):
    return date.strftime("%B %d, %Y %H:%M")

jinja_environment.filters['get_user'] = get_user
jinja_environment.filters['convert_date'] = convert_date



"""Request Handlers Start Here"""


class BaseHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.now = datetime.datetime.now()
        self.tv = {}
        self.settings = SETTINGS.copy()
        self.sb_locations = SAFEBOX_LOCATIONS.copy()
        self.initialize(request, response)
        self.has_pass = False
        self.tv["version"] = os.environ['CURRENT_VERSION_ID']
        self.local = False
        if "127.0.0.1" in self.request.uri or "localhost" in self.request.uri:
            self.local = True
        # misc
        self.tv["current_url"] = self.request.uri
        # self.tv["fb_login_url"] = facebook.generate_login_url(self.request.path, self.uri_for('www-fblogin'))

        if "?" in self.request.uri:
            self.tv["current_base_url"] = self.request.uri[0:(self.request.uri.find('?'))]
        else:
            self.tv["current_base_url"] = self.request.uri

        try:
            self.tv["safe_current_base_url"] = urllib.quote(self.tv["current_base_url"])
        except:
            logging.exception("safe url error")

        self.tv["request_method"] = self.request.method

        self.session = self.get_session()
        self.user = self.get_current_user()


    def render(self, template_path=None, force=False):
        self.tv["current_timestamp"] = time.mktime(self.now.timetuple())
        self.settings["current_year"] = self.now.year
        self.tv["settings"] = self.settings
        self.tv["sb_locations"] = self.sb_locations
        self.tv["date_today"] = datetime.datetime.now().strftime("%m/%d/%Y")


        if self.request.get('error'):
            self.tv["error"] = self.request.get("error").strip()
        if self.request.get('success'):
            self.tv["success"] = self.request.get("success").strip()
        if self.request.get('warning'):
            self.tv["warning"] = self.request.get("warning").strip()
        if self.request.get('goto'):
            self.tv["goto"] = self.request.get("goto").strip()

        if self.user:
            self.tv["user"] = self.user.to_object()

        if self.request.get('json') or not template_path:
            self.response.out.write(simplejson.dumps(self.tv))
            return

        template = jinja_environment.get_template(template_path)
        self.response.out.write(template.render(self.tv))
        logging.debug(self.tv)


    def get_session(self):
        from gaesessions import get_current_session
        return get_current_session()


    def get_current_user(self):
        if self.session.has_key("user"):
            user = User.get_by_id(self.session["user"])
            return user
        else:
            return None


    def login(self, user):
        self.session["user"] = user.key.id()
        return

    def login_fb(self, fb_content, access_token):
        self.logout()
        user = User.query(User.fb_id == fb_content["id"]).get()
        if not user:
            email = fb_content["email"]
            if email:
                user = User.query(User.email == email).get()

            if user:
                # Merge User

                user.fb_id = fb_content["id"]
                try:
                    user.fb_username = fb_content["username"]
                except:
                    logging.exception("no username?")
                user.first_name = fb_content["first_name"]
                try:
                    user.last_name = fb_content["last_name"]
                except:
                    logging.exception("no last_name?")
                try:
                    user.middle_name = fb_content["middle_name"]
                except:
                    logging.exception('no middle name?')

                user.name = user.first_name
                if user.middle_name:
                    user.name += " " + user.middle_name

                if user.last_name:
                    user.name += " " + user.last_name

                try:
                    user.fb_access_token = access_token
                except:
                    logging.exception('no access token')
            else:
                user = User(id=email)
                user.fb_id = fb_content["id"]
                try:
                    user.fb_username = fb_content["username"]
                except:
                    logging.exception("no username?")
                user.email = fb_content["email"]
                user.first_name = fb_content["first_name"]
                try:
                    user.last_name = fb_content["last_name"]
                except:
                    logging.exception("no last_name?")
                try:
                    user.middle_name = fb_content["middle_name"]
                except:
                    logging.exception('no middle name?')

                user.name = user.first_name
                if user.middle_name:
                    user.name += " " + user.middle_name

                if user.last_name:
                    user.name += " " + user.last_name

                try:
                    user.fb_access_token = access_token
                except:
                    logging.exception('no access token')

            user.put()
        self.login(user)
        return


    def logout(self):
        if self.session.is_active():
            self.session.terminate()
            return


    def iptolocation(self):
        country = self.request.headers.get('X-AppEngine-Country')
        logging.info("COUNTRY: " + str(country))
        if country == "GB":
            country = "UK"
        if country == "ZZ":
            country = ""
        if country is None:
            country = ""
        return country


class ErrorHandler(BaseHandler):
    def get(self, page):
        self.tv["current_page"] = "ERROR"
        self.render('frontend/dynamic404.html')


# class StickyNotesHandler(BaseHandler):
#     def get(self):
#         self.render("frontend/sticky-notes.html")

class FrontPage(BaseHandler):
    def get(self):
        if self.user:
            self.redirect(self.uri_for('www-dashboard-admin'))
            return

        self.tv["current_page"] = "FRONT"
        self.render('frontend/front.html')

class ServicePage(BaseHandler):
    def get(self):
        if self.user:
            self.redirect(self.uri_for('www-dashboard-admin'))
            return

        self.tv["current_page"] = "FRONT"
        self.render('frontend/service.html')

class PortfolioPage(BaseHandler):
    def get(self):
        if self.user:
            self.redirect(self.uri_for('www-dashboard-admin'))
            return
        portfolios = Portfolio.query().fetch()
        self.tv["portfolios"] = []
        for this_data in portfolios:
            self.tv["portfolios"].append(this_data.to_object())

        self.tv["current_page"] = "PORTFOLIO"
        self.render('frontend/portfolio.html')

class AboutPage(BaseHandler):
    def get(self):
        if self.user:
            self.redirect(self.uri_for('www-dashboard-admin'))
            return

        abouts = About.query().fetch()
        self.tv["abouts"] = []
        for this_data in abouts:
            self.tv["abouts"].append(this_data.to_object())

        self.tv["current_page"] = "FRONT"
        self.render('frontend/about.html')

class ContactPage(BaseHandler):
    def get(self):
        if self.user:
            self.redirect(self.uri_for('www-dashboard-admin'))
            return

        self.tv["current_page"] = "FRONT"
        self.render('frontend/contact.html')

class RequestPage(BaseHandler):
    def get(self):
        if self.user:
            self.redirect(self.uri_for('www-dashboard-admin'))
            return

        self.tv["current_page"] = "REQUEST"
        self.render('frontend/request.html')        

class PandCoPage(BaseHandler):
    def get(self):
        if self.user:
            self.redirect(self.uri_for('www-dashboard-admin'))
            return

        self.tv["current_page"] = "SINGLE"
        self.render('frontend/pandco.html')        

class DeppoPage(BaseHandler):
    def get(self):
        if self.user:
            self.redirect(self.uri_for('www-dashboard-admin'))
            return

        self.tv["current_page"] = "SINGLE"
        self.render('frontend/deppo.html')        

class LoginPage(BaseHandler):
    def get(self):
        if self.user:
            self.redirect(self.uri_for('www-dashboard-admin'))
            return

        if self.request.get('email'):
            self.tv["email"] = self.request.get('email').strip()                    

        self.tv["current_page"] = "LOGIN"
        self.render('frontend/login.html')

    def post(self):
        if self.user:
            self.redirect(self.uri_for('www-dashboard-admin'))
            return

        if self.request.get('email') and self.request.get('password'):
            email = self.request.get('email').strip().lower()
            password = self.request.get('password')
            user = User.get_by_id(self.request.get("email"))
            
            if not user:
                self.redirect(self.uri_for('www-login', error="User not found. Please try another email or register."))
                return
            if user.password == hash_password(email, password):
                self.login(user)
                if self.request.get('goto'):
                    self.redirect(self.request.get('goto'))
                else:
                    self.redirect(self.uri_for('www-dashboard-admin'))
                return
            else:
                self.redirect(self.uri_for('www-login', error="Wrong password. Please try again.", email=email))
                return
        else:
            self.redirect(self.uri_for('www-login', error="Please enter your email and password."))

class RegistrationPage(BaseHandler):
    def get(self):
        if self.user:
            self.redirect(self.uri_for('www-dashboard-admin', referred="register"))
            return

        self.tv["current_page"] = "REGISTER"
        self.render("frontend/register.html")

    def post(self):
        if self.user:
            self.redirect(self.uri_for('www-dashboard-admin'))
            return

        if self.request.get('email') and self.request.get('first_name') and self.request.get('last_name') and self.request.get('password'):
            email = self.request.get('email').strip().lower()
            name = self.request.get('first_name') + " " + self.request.get('last_name')
            phone = self.request.get('phone')
            password = self.request.get('password')
            user = User.get_by_id(email)
            if user:
                self.redirect(self.uri_for('www-register', error="User already exist. Please log in."))
                return

            user = User(id=email)
            user.email = email
            user.password = hash_password(email, password)            
            user.name = name
            user.phone = phone

            user.put()
            self.login(user)
            if self.request.get('goto'):
                self.redirect(self.request.get('goto'))
            else:
                self.redirect(self.uri_for('www-dashboard-admin'))
            return
        else:
            self.redirect(self.uri_for('www-register', Error="Please enter the all information required."))

class SubscribeHandler(BaseHandler):
    def get(self):
        self.render("frontend/thankyoupage.html")

    def post(self):
        email = self.request.get("email").strip()
        token = str(uuid.uuid4())
        user = SubscribedEmails.query(SubscribedEmails.email == email).fetch(1)
        if not user:
            while True:
                user = SubscribedEmails(id=token)
                user.email = email
                user.token = token
                user.put()
                if user:
                    break

            logging.critical("saving...")
            send_email_subscription(email, user.token)
            self.redirect(self.uri_for("www-front", msg="Thank you for subscribing us!."))
        else:
            self.redirect(self.uri_for("www-front", error="Email Already Exist."))
            return

class QuoteHandler(BaseHandler):
    def get(self):
        self.render("frontend/request.html")

    def post(self):
        if self.request.get("name") and self.request.get("country") and self.request.get("email") and self.request.get("service_type") and self.request.get("web_type"):
            email = self.request.get("email").strip()            
            name = self.request.get("name")
            proj_title = self.request.get("proj_title")
            company = self.request.get("company")
            country = self.request.get("country")
            phone = self.request.get("phone")
            service_type = self.request.get("service_type")
            web_type = self.request.get("web_type")
            competitor_site = self.request.get("competitor_site")
            interest_site = self.request.get("interest_site")
            proj_desc = self.request.get("proj_desc")
            
            user = RequestQuote(id=email)
            user.name = name
            user.email = email
            user.company = company
            user.country = country
            user.proj_title = proj_title
            user.phone = phone
            user.service_type = service_type
            user.web_type = web_type
            user.competitor_site = competitor_site
            user.interest_site = interest_site
            user.proj_desc = proj_desc
            user.put()

            send_email_request(email, name, company, country, phone, service_type, web_type, proj_title, proj_desc, interest_site, competitor_site)

            self.redirect(self.uri_for('www-request', msg = "Thank you for making a request with us!, you'll be a touched with our project managers as soon as they get your proposal."))
        else:
            self.redirect(self.uri_for('www-request', error = "Please enter all the information required."))

class DashboardPage(BaseHandler):
    @login_required
    def get(self):
        if self.user.status == "user":
            self.tv["current_page"] = "DASHBOARD"
            self.render('frontend/dashboard.html')
        elif self.user.status == "admin":
            self.tv["current_page"] = "ADMIN DASHBOARD"
            self.render('frontend/dashboard-admin.html')
class AdminDashboardPage(BaseHandler):
    @login_required
    def get(self):
        homes = Home.query().fetch()
        self.tv["homes"] = []
        for this_data in homes:
            self.tv["homes"].append(this_data.to_object())
        self.tv["current_page"] = "ADMIN DASHBObARD"
        self.render('frontend/dashboard-admin.html')
    @login_required
    def post(self):
        home_id = self.request.get("this_id")
        newHome = Home.get_by_id(int(home_id))
        # newHome.title = self.request.get("title").strip()
        # newHome.description = self.request.get("description").strip()
        logging.critical("title: "+self.request.get("editTitle").strip()+"----------------------------")
        logging.critical("description: "+self.request.get("title").strip()+"----------------------------")
        #newHome.put()
        self.redirect(self.uri_for('www-dashboard-admin'))
    @login_required
    def delete(self):
        home_id = self.request.get("this_id")
        home_id = Home.get_by_id(int(home_id))
        home_id.key.delete()
class HomeCreatePage(BaseHandler):
    @login_required
    def get(self):
        self.tv["current_page"] = "ADD HOME"
        self.render('frontend/home-createlist.html')
    # @login_required
    # def post(self):
    #     newHome = Home()
    #     newHome.title = self.request.get("title")
    #     newHome.description = self.request.get("description")
    #     newHome.put()
    #     self.render('frontend/home-createlist.html')
class PortfolioCreatePage(BaseHandler):
    @login_required
    def get(self):        
        self.tv["current_page"] = "ADD PORTFOLIO"
        self.render('frontend/portfolio-createlist.html')
    @login_required
    def post(self):
        newPortfolio = Portfolio()
        newPortfolio.title = self.request.get("title")
        newPortfolio.description = self.request.get("description")
        newPortfolio.put()
        self.render('frontend/portfolio-createlist.html')
class PortfolioEditPage(BaseHandler):
    @login_required
    def get(self):
        portfolios = Portfolio.query().fetch()
        self.tv["portfolios"] = []
        for this_data in portfolios:
            self.tv["portfolios"].append(this_data.to_object())
        self.tv["current_page"] = "EDIT PORTFOLIO"
        self.render('frontend/portfolio-edit.html')
    @login_required
    def delete(self):
        portfolio_id = self.request.get("this_id")
        portfolio_id = Portfolio.get_by_id(int(portfolio_id))
        portfolio_id.key.delete()
class AboutCreatePage(BaseHandler):
    @login_required
    def get(self):        
        self.tv["current_page"] = "ADD ABOUT"
        self.render('frontend/about-createlist.html')
    @login_required
    def post(self):
        newAbout = About()
        newAbout.name = self.request.get("full_name")
        newAbout.position = self.request.get("position")
        newAbout.description = self.request.get("description")
        newAbout.put()
        self.render('frontend/about-createlist.html')
class AboutEditPage(BaseHandler):
    @login_required
    def get(self):
        abouts = About.query().fetch()
        self.tv["abouts"] = []
        for this_data in abouts:
            self.tv["abouts"].append(this_data.to_object())
        self.tv["current_page"] = "EDIT ABOUT"
        self.render('frontend/about-edit.html')
class ViewServicePage(BaseHandler):
    @login_required
    def get(self):

        # Web Design Display
        web_design = ServiceWebDesign.query().fetch()
        self.tv["web_design"] = []
        for this_data in web_design:
            self.tv["web_design"].append(this_data.to_object())
        # Mobile Dev Display
        mobile_dev = ServiceMobileDev.query().fetch()
        self.tv["mobile_dev"] = []
        for this_data in mobile_dev:
            self.tv["mobile_dev"].append(this_data.to_object())

        self.tv["current_page"] = "VIEW SERVICE"
        self.render('frontend/service-view.html')
class CreateServicePage(BaseHandler):
    @login_required
    def get(self):        
        self.tv["current_page"] = "ADD PORTFOLIO"
        self.render('frontend/www-service-createlist.html')
    @login_required
    def post(self):
        newService = Service()
        newService.title = self.request.get("title")
        newService.description = self.request.get("description")
        newService.put()
        self.render('frontend/www-service-createlist.html')
class WebDesignServicePage(BaseHandler):
    @login_required
    def get(self):        
        self.tv["current_page"] = "WEB DESIGN"
        self.render('frontend/service-webdesign.html')
    @login_required
    def post(self):
        newWeb = ServiceWebDesign()
        newWeb.title = self.request.get("title")
        newWeb.description = self.request.get("description")
        newWeb.put()
        self.render('frontend/service-webdesign.html')
class MobileDevServicePage(BaseHandler):
    @login_required
    def get(self):        
        self.tv["current_page"] = "MOBILE DEV"
        self.render('frontend/service-mobiledev.html')
    @login_required
    def post(self):
        newMobile = ServiceMobileDev()
        newMobile.title = self.request.get("title")
        newMobile.description = self.request.get("description")
        newMobile.put()
        self.render('frontend/service-mobiledev.html')
class Logout(BaseHandler):
    def get(self):
        if self.user:
            self.logout()
        self.redirect(self.uri_for('www-front', referred="logout"))

site_domain = SETTINGS["site_domain"].replace(".","\.")

app = webapp2.WSGIApplication([
    routes.DomainRoute(r'<:' + site_domain + '|localhost|' + SETTINGS["app_id"] + '\.appspot\.com>', [
        webapp2.Route('/', handler=FrontPage, name="www-front"),
        webapp2.Route('/service', handler=ServicePage, name="www-service"),
        webapp2.Route('/request', handler=RequestPage, name="www-request"),
        webapp2.Route('/portfolio', handler=PortfolioPage, name="www-portfolio"),
        webapp2.Route('/about', handler=AboutPage, name="www-about"),
        webapp2.Route('/pandco', handler=PandCoPage, name="www-single"),
        webapp2.Route('/deppo', handler=DeppoPage, name="www-single"),
        webapp2.Route('/contact', handler=ContactPage, name="www-contact"),
        webapp2.Route('/subscribe', handler=SubscribeHandler, name="www-subscribe"),
        webapp2.Route('/quote', handler=QuoteHandler, name="www-quote"),
        webapp2.Route('/login', handler=LoginPage, name="www-login"),
        webapp2.Route('/register', handler=RegistrationPage, name="www-register"),
        webapp2.Route('/dashboard', handler=DashboardPage, name="www-dashboard"),
        webapp2.Route('/dashboard-admin', handler=AdminDashboardPage, name="www-dashboard-admin"),
        webapp2.Route('/logout', handler=Logout, name="www-logout"),
        webapp2.Route('/home-createlist', handler=HomeCreatePage, name="www-home-createlist"), 
        webapp2.Route('/portfolio-createlist', handler=PortfolioCreatePage, name="www-portfolio-createlist"),
        webapp2.Route('/portfolio-edit', handler=PortfolioEditPage, name="www-portfolio-edit"),
        webapp2.Route('/about-createlist', handler=AboutCreatePage, name="www-about-createlist"),
        webapp2.Route('/about-edit', handler=AboutEditPage, name="www-about-edit"),
        webapp2.Route('/service-view', handler=ViewServicePage, name="www-service-view"),
        webapp2.Route('/service-createlist', handler=CreateServicePage, name="www-service-createlist"),
        webapp2.Route('/service-webdesign', handler=WebDesignServicePage, name="www-service-webdesign"),
        webapp2.Route('/service-mobiledev', handler=MobileDevServicePage, name="www-service-mobiledev"),
        # webapp2.Route('/sticky-notes', handler=StickyNotesHandler, name="www-sticky-notes"),


        webapp2.Route(r'/<:.*>', ErrorHandler)
    ])
])

# if RAYGUN_API_KEY:
#     app.error_handlers[500] = log_exception
#     app.error_handlers[405] = log_404
#     app.error_handlers[404] = log_404
