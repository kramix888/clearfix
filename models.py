from google.appengine.ext import ndb
import time
import logging

class User(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    phone = ndb.StringProperty()
    name = ndb.StringProperty()
    status = ndb.StringProperty(default="admin")
    
    def to_object(self):
        details = {}
        details["created"] = int(time.mktime(self.created.timetuple()))
        details["updated"] = int(time.mktime(self.updated.timetuple()))
        details["email"] = self.email
        details["password"] = self.password
        details["phone"] = self.phone
        details["name"] = self.name
        details["status"] = self.status
        return details

class SubscribedEmails(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now_add=True)
    email = ndb.StringProperty(required=True)
    token = ndb.StringProperty(required=True)
    registered = ndb.BooleanProperty(default=False)

class RequestQuote(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now_add=True)
    quote_code = ndb.StringProperty()
    name = ndb.StringProperty(required=True)
    company = ndb.StringProperty()
    country = ndb.StringProperty(required=True)
    phone = ndb.StringProperty()
    email = ndb.StringProperty(required=True)
    service_type = ndb.StringProperty(required=True)
    web_type = ndb.StringProperty(required=True)
    competitor_site = ndb.StringProperty()
    interest_site = ndb.StringProperty()
    proj_title = ndb.StringProperty()
    proj_desc = ndb.StringProperty()

    def to_object(self):
        details = {}
        details["created"] = int(time.mktime(self.created.timetuple()))
        details["updated"] = int(time.mktime(self.created.timetuple()))
        details["name"] = self.name
        details["company"] = self.company
        details["country"] = self.country
        details["phone"] = self.phone
        details["email"] = self.email
        details["service_type"] = self.service_type
        details["web_type"] = self.web_type
        details["competitor_site"] = self.competitor_site
        details["interest_site"] = self.interest_site
        details["proj_title"] = self.proj_title
        details["proj_desc"] = self.proj_desc
        return details
class Home(ndb.Model):   
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now_add=True)
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    
    def to_object(self):
        details = {}
        details["created"] = int(time.mktime(self.created.timetuple()))
        details["updated"] = int(time.mktime(self.created.timetuple()))
        details["id"] = self.key.id()
        details["title"] = self.title
        details["description"] = self.description
        return details
class HomeSlider(ndb.Model):   
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now_add=True)
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    
    def to_object(self):
        details = {}
        details["created"] = int(time.mktime(self.created.timetuple()))
        details["updated"] = int(time.mktime(self.created.timetuple()))
        details["id"] = self.key.id()
        details["title"] = self.title
        details["description"] = self.description
        return details
class Portfolio(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now_add=True)
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    
    def to_object(self):
        details = {}
        details["created"] = int(time.mktime(self.created.timetuple()))
        details["updated"] = int(time.mktime(self.created.timetuple()))
        details["id"] = self.key.id()
        details["title"] = self.title
        details["description"] = self.description
        return details
class Service(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now_add=True)
    header = ndb.StringProperty()
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    
    def to_object(self):
        details = {}
        details["created"] = int(time.mktime(self.created.timetuple()))
        details["updated"] = int(time.mktime(self.created.timetuple()))
        details["id"] = self.key.id()
        details["header"] = self.header
        details["title"] = self.title
        details["description"] = self.description
        return details
class ServiceWebDesign(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now_add=True)
    header = ndb.StringProperty()
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    
    def to_object(self):
        details = {}
        details["created"] = int(time.mktime(self.created.timetuple()))
        details["updated"] = int(time.mktime(self.created.timetuple()))
        details["id"] = self.key.id()
        details["header"] = self.header
        details["title"] = self.title
        details["description"] = self.description
        return details
class ServiceMobileDev(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now_add=True)
    header = ndb.StringProperty()
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    
    def to_object(self):
        details = {}
        details["created"] = int(time.mktime(self.created.timetuple()))
        details["updated"] = int(time.mktime(self.created.timetuple()))
        details["id"] = self.key.id()
        details["header"] = self.header
        details["title"] = self.title
        details["description"] = self.description
        return details
class About(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now_add=True)
    name = ndb.StringProperty()
    position = ndb.StringProperty()
    description = ndb.StringProperty()
    
    def to_object(self):
        details = {}
        details["created"] = int(time.mktime(self.created.timetuple()))
        details["updated"] = int(time.mktime(self.created.timetuple()))
        details["id"] = self.key.id()
        details["name"] = self.name
        details["position"] = self.position
        details["description"] = self.description
        return details