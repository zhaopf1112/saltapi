import requests
import json
import httplib
import logging
import logging.handlers

IP_PORT = 'ip:port'
LOG_FILE = "/var/log/salt-api.log"
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=20 * 1024 * 1024, backupCount=5)
fmt = "%(asctime)s - %(name)s - [%(filename)s:%(lineno)s] - %(levelname)s - %(message)s "
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger('salt-api')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def token_get():

    token_info = httplib.HTTPConnection(IP_PORT)
    api_dir = "/login"

    body_message = {"username":"xxx","password": "xxx","eauth": "pam"}
    token_info.request("POST",api_dir,body=json.dumps(body_message),headers={"Content-Type":"application/json"})
    token_message = token_info.getresponse()
    tt_ = token_message.read()
    zz = eval(tt_)['return'][0]['token']
    token_info.close()
    return zz

def async(tt_, tgt, fun, args=[]):

    url_connect = httplib.HTTPConnection(IP_PORT)
    api_dir = "/"
    body_params = {'client': 'local_async', 'fun': fun, 'tgt': tgt, 'arg':args}
    headers_ = {"Content-Type":"application/json", 'X-Auth-Token': tt_}
    try:
        url_connect.request("POST",api_dir,body=json.dumps(body_params),headers=headers_)
        response_message = url_connect.getresponse()
        result_info = response_message.read()
        rr = json.loads(result_info)
        url_connect.close()
        return rr['return'][0]['jid']
    except Exception as err:
        print err
         
def jobs_all(tt_, jid=None):
    headers = {"Content-Type":"application/json", 'X-Auth-Token': tt_}
    try:
        if jid is None:
            ret = requests.get('http://'+IP_PORT+'/jobs', headers=headers, verify=False)
        else:
            ret = requests.get('http://'+IP_PORT+'/jobs/'+jid, headers=headers, verify=False)
            ret.close()
        ret = json.loads(ret.text)
        print ret['info'][0]
        logger.debug(ret['info'][0])
        logger.debug(ret['info'][0]['Function'])
        logger.debug(ret['info'][0]['Arguments'])
  
        return ret
    except Exception as err:
        logger.error(err)


if __name__ == "__main__":
  tt_ = token_get()         
  jid = async(tt_, 'mesos*', 'cmd.run', args=['df -h'])
  jobs_all(tt_, jid=jidD
