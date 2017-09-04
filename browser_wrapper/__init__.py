import requests
import shutil
from browser_errors import UnauthenticatedUserError, RequestWithoutDefaultParamsError, UninitializedWorkerError

class BrowserStack(object):
    """Main BS class. All methods would be encapsulated within this"""

    def __init__(self, username=None, access_key=None):
        """
        Constructor for the BrowserStack class, returns a aunthenticated object

        :param username:
        :param access_key:
        """
        self.base_url = 'https://api.browserstack.com/4'
        self.authorized = False
        self.worker_id = []
        if username==None or access_key==None:
            raise UnauthenticatedUserError("Could not authenticate user, please check your tokens and try again")
        else:
            r = requests.get(self.base_url, auth=(username, access_key))
            if r.status_code == 200:
                self.username = username
                self.access_key = access_key
                self.authorized = True
            elif r.status_code != 200:
                raise UnauthenticatedUserError("Could not authenticate user, please check your tokens and try again")

    def get_available_browsers(self, flat=False, get_all=False):
        available_browser_url = "/browsers"
        if self.authorized:
            session  = requests.Session()
            session.auth = (self.username,self.access_key)
            if flat and get_all:
                available_browser = session.get(self.base_url+ available_browser_url + "?flat=true&all=true")
            elif flat==True and get_all==False:
                available_browser = session.get(self.base_url + available_browser_url + "?flat=true")
            elif flat==False and get_all==True:
                available_browser = session.get(self.base_url + available_browser_url + "?all=true")
            else:
                available_browser = session.get(self.base_url+ available_browser_url)
            return  available_browser.json()
        else:
            raise UnauthenticatedUserError("Unauthenticated user, please authenticate and try again")

    def new_worker(self, os=None, os_version=None, url=None, browser=None, browser_version=None, timeout=300,device=None,
                   name=None, build=None, project=None, browserstack_video=None):
        if self.authorized:
            if os==None or os_version==None or url==None:
                raise RequestWithoutDefaultParamsError("Default params not provided, please provide default params and try again")

            session = requests.Session()
            session.auth = (self.username, self.access_key)
            DESKTOP_OS_VERSIONS = ['OS X', 'Windows']

            if os_version in DESKTOP_OS_VERSIONS and (browser==None or browser_version==None):
                raise RequestWithoutDefaultParamsError(
                    "Default params not provided, please provide default params and try again")

            # add right params
            data = {}
            data['os'] = os
            data['os_version'] = os_version
            data['url'] = url
            if browser is not None:
                data['browser'] = browser
            if browser_version is not  None:
                data['browser_version'] = browser_version
            if timeout is not None:
                data['timeout'] = timeout
            if device is not None:
                data['device'] = device
            if name is not None:
                data['name'] = name
            if build is not None:
                data['build'] = build
            if project is not None:
                data['project'] = project
            if browserstack_video is not None:
                data['browserstack.video'] = browserstack_video
            resp = session.post(self.base_url + '/worker', data=data)
            if resp.status_code == 200:
                resp_json = resp.json()
                self.worker_id.append(resp_json['id'])
                return resp_json
            else:
                raise RequestWithoutDefaultParamsError("Inavlid params passed")

        else:
            raise UnauthenticatedUserError("Unauthenticated user, please authenticate and try again")

    def worker_screenshot(self, worker_id):

        if self.authorized:
            if int(worker_id) in self.worker_id:
                session = requests.Session()
                session.auth = (self.username, self.access_key)
                resp =session.get(self.base_url + '/worker/{}/screenshot.png'.format(worker_id), stream=True)

                if resp.status_code == 200:
                    with open('screenshot.png', 'wb') as out_file:
                        shutil.copyfileobj(resp.raw, out_file)
                    print "Successfully saved screenshot"
                else:
                    raise UninitializedWorkerError("Worker not found")
            else:
                raise UninitializedWorkerError("Worker not initialized, please create a worker first")
        else:
            raise UnauthenticatedUserError("Unauthenticated user, please authenticate and try again")

    def delete_worker(self, worker_id):
        if self.authorized:
            if int(worker_id) in self.worker_id:
                session = requests.Session()
                session.auth = (self.username, self.access_key)
                resp = session.delete(self.base_url+'/worker/{}'.format(worker_id))

                if resp.status_code == 200:
                    resp_json = resp.json()
                    print "Worker ran for {} seconds".format(resp_json['time'])
                else:
                    raise UninitializedWorkerError("Invalid worker")
            else:
                raise UninitializedWorkerError("Worker not initialized, please create a worker first")
        else:
            raise UnauthenticatedUserError("Unauthenticated user, please authenticate and try again")

    def get_single_worker_status(self,worker_id):
        if self.authorized:
            if int(worker_id) in self.worker_id:
                session = requests.Session()
                session.auth = (self.username, self.access_key)
                resp = session.get(self.base_url + '/worker/{}'.format(worker_id))
                if resp.status_code == 200:
                    resp_json = resp.json()
                    if resp_json:
                        return resp_json
                    else:
                        print "Worker terminated"
                else:
                    raise UninitializedWorkerError("Invalid worker")
            else:
                raise UninitializedWorkerError("Worker not initialized, please create a worker first")
        else:
            raise UnauthenticatedUserError("Unauthenticated user, please authenticate and try again")

    def get_worker_status(self):
        if self.authorized:
            session = requests.Session()
            session.auth = (self.username, self.access_key)
            resp = session.get(self.base_url + '/workers')
            if resp.status_code == 200:
                resp_json = resp.json()
                if resp_json:
                    return resp_json
                else:
                    print "Worker data not found"
            else:
                raise UninitializedWorkerError("Workers not defined")
        else:
            raise UnauthenticatedUserError("Unauthenticated user, please authenticate and try again")

    def get_api_status(self):
        if self.authorized:
            session = requests.Session()
            session.auth = (self.username, self.access_key)
            resp = session.get(self.base_url + '/status')
            if resp.status_code == 200:
                resp_json = resp.json()
                if resp_json:
                    return resp_json
                else:
                    print "Could not find API status data"
            else:
                raise UninitializedWorkerError("Workers not defined")
        else:
            raise UnauthenticatedUserError("Unauthenticated user, please authenticate and try again")