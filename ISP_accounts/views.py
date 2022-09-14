from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
# Create your views here.

# from django.shortcuts import  render, redirect
# from .login import NewUserForm
# from django.contrib.auth import login
# from django.contrib import messages

# def register_request(request):
# 	if request.method == "POST":
# 		form = NewUserForm(request.POST)
# 		if form.is_valid():
# 			user = form.save()
# 			login(request, user)
# 			messages.success(request, "Registration successful." )
# 			return redirect("main:homepage")
# 		messages.error(request, "Unsuccessful registration. Invalid information.")
# 	form = NewUserForm()
# 	return render (request=request, template_name="test.html", context={"register_form":form})


from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
import sys, time, datetime, os
import logging, requests, xmltodict
import imaplib, poplib
def index(request):
    return render(request,'index.html')




import sys, time, datetime, os
import logging, requests, xmltodict
import imaplib, poplib


def run_webservice_api(apiURL, timeout=None):
    try:
        response = requests.get(apiURL, timeout=10 if not timeout else timeout)
        if response.status_code!=200:
            return False, "Exception# Service Unreachable with status code: {}".format(response.status_code)
        return True, response
    except requests.exceptions.Timeout:
        return False, "Service Unreachable, Can You Reload this page, If the problem persists, contact support"        
    except requests.exceptions.RequestException as e:
        return False, "Exception# running remote webservice api [{}]".format(e) 

def autodiscover_thunderbird(domain, domain_name):
    incomingServer = None
    autoconfig_url = "https://autoconfig.thunderbird.net/v1.1/%s"%(domain_name)
    status, data = run_webservice_api(autoconfig_url)
    if status:
        xpars = xmltodict.parse(data.text)
        for row in  xpars["clientConfig"]["emailProvider"]["incomingServer"]:
            if row["@type"] in ["imap", "pop3"]:
                incomingServer = {"inbox": "INBOX", "spam": None}
                incomingServer["server"] = row["hostname"]
                incomingServer["port"] = int(row["port"])
                incomingServer["use_ssl"] = True if row["socketType"] == 'SSL' else False
                incomingServer["is_pop"] = False if row["@type"] == "imap" else True
    else:
        logging.error(data)
    
    return incomingServer
def autodiscover_firetrust(domain_name):
    incomingServer = None
    autoconfig_url = "https://emailsettings.firetrust.com/settings?q=test.user@%s"%(domain_name)
    status, data = run_webservice_api(autoconfig_url)
    if status:
        xparse = data.json()
        for row in xparse["settings"]:
            if row["protocol"] == "IMAP":
                incomingServer = {"inbox": "INBOX", "spam": None}
                incomingServer["server"] = row["address"]
                incomingServer["port"] = int(row["port"])
                incomingServer["use_ssl"] = True if row["secure"] == 'SSL' else False
                incomingServer["is_pop"] = False
            elif row["protocol"] == "POP3":
                incomingServer = {"inbox": "INBOX", "spam": None}
                incomingServer["server"] = row["address"]
                incomingServer["port"] = int(row["port"])
                incomingServer["use_ssl"] = True if row["secure"] == 'SSL' else False
                incomingServer["is_pop"] = True
    else:
        logging.error(data)

    return incomingServer

class ImapPopLib():
    def __init__(self, username, password, imapPop_config):
        self.imapPop_config = imapPop_config
        self.use_ssl = imapPop_config["use_ssl"]
        self.server = str(imapPop_config["server"])
        self.port = imapPop_config["port"]
        self.is_pop = True if imapPop_config["is_pop"] else False
        self.username = username
        self.password = password

    def login(self):
        logging.info( "Try to Login %s email"%(self.username))
        try:
            if self.is_pop:
                self.pop = poplib.POP3_SSL(self.server, self.port) if self.use_ssl else  poplib.POP3(self.server, self.port)
                try:
                    self.pop.user(self.username)
                    self.pop.pass_(self.password)
                    msgs=self.pop.list()#id size
                    self.messages_ids = [ int(m.split()[0]) for m in msgs[1]]
                    logging.info( "Successfully logged-"+self.username)
                    self.logout()
                    return True
                
                except Exception as  e:
                    logging.error( "can't connect !!!-%s"%(e))  
            else: 
                self.imap = imaplib.IMAP4_SSL(self.server, self.port) if self.use_ssl else imaplib.IMAP4(self.server, self.port)
                status, data  = self.imap.login(self.username, self.password)
                if status == 'OK':
                    logging.info( "Successfully logged-"+self.username)
                    self.logout()
                    return True

                else:
                    logging.error( "can't connect !!!-%s"%(data))  

        except Exception as e:
                logging.error("Exception connection/login: %s"%(e))
    
        return False
    
    def logout(self):
        try:
            if self.is_pop: self.pop.quit()
            else: self.imap.logout()
        except:
            pass 
        


# from django.views.decorators.csrf import csrf_protect

# @csrf_protect
def login(request):
    # if request.user.is_authenticated:
    # 	return render(request, 'index.html', {})

    # csrfContext = RequestContext(request)

    if request.method == 'POST':

        username = request.POST.get('email')
        password = request.POST.get('password')

        logging.basicConfig(level=logging.INFO)
        logging.info("Start")
        
        domain_name = username.split('@')[1]
        logging.info("> DomainName: %s"%domain_name)


        incomingServer = autodiscover_firetrust(domain_name)
        print("SERVER",incomingServer)

        if incomingServer:
            incoming_lib = ImapPopLib(username, password, incomingServer)
            incoming_lib.login()

        print(incoming_lib.is_pop)
       

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)
                auth_login(request, user)
            if request.POST.get("next"):
                return redirect(request.POST.get("next"))
            return redirect('home')
        else:
            messages.error(request, "Les informations que vous venez d'entrer sont incorrects. Veuillez réessayer.")
            return render(request, 'index.html', {})
    return render(request, 'index.html', {})

    

from rest_framework.views import APIView
from rest_framework.response import Response

class HelloView(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)