from xrd import XRD
import re
import urllib, urllib2

#
# get webfinger response
#

ACCT_RE = re.compile(r'acct:([\w_.]+)@([\w:_.]+)')
URLTEMPLATE_RE = re.compile(r'\{(%?)(id|uri|userinfo|host)\}')

def _var_replacer(email):    
    (local, host) = email.split('@')
    uri = 'acct:%s' % email
    rvars = {
        'id': uri,  # deprecated on 9/17/2009
        'uri': uri,
        'userinfo': local,
        'host': host,
    }
    def _replacer(match):
        (encode, var) = match.groups()
        val = rvars[var]
        if encode == '%':
            val = urllib.quote_plus(val)
        return val
    return _replacer

def finger(email, raw=False):
    
    # 1) resolve host-meta URL for acct URI
    
    (local, host) = email.split('@')
    hostmeta_url = "http://%s/.well-known/host-meta" % host
    
    # 2) obtain host-meta file
    
    redirect_handler = urllib2.HTTPRedirectHandler()
    opener = urllib2.build_opener(redirect_handler)
    opener.addheaders = [('User-agent', 'python-webfinger')]
    conn = opener.open(hostmeta_url)
    xrd = XRD.parse(conn.read())
    #xrd = XRD.parse(open('example_hostmeta.xml').read())
    conn.close()
    
    # verify resource.host == host
    
    webfinger_types = (
        'http://webfinger.net/rel/acct-desc',   # current
        'http://webfinger.info/rel/service',    # deprecated on 9/17/2009
        'lrdd',                                 # used by Google
    )
    
    links = [link for link in xrd.links if link.rel in webfinger_types]

    if links:

        xrd_url = URLTEMPLATE_RE.sub(_var_replacer(email),  links[0].template)
        
        conn = opener.open(xrd_url)
        xrd_response = conn.read() if raw else XRD.parse(conn.read())
        conn.close()
        
        return xrd_response

#
# methods to parse finger response
#
        
def _link(resource, rel, type_=None):
    for link in resource.links:
        if link.rel == rel and (type_ is None or link.type == type_):
            return link.href

def service(resource):
    return _link(resource, 'http://portablecontacts.net/spec/1.0')

def profile(resource):
    return _link(resource, 'http://webfinger.net/rel/profile-page')

def hcard(resource):
    return _link(resource, 'http://microformats.org/profile/hcard')

def openid(resource):
    return _link(resource, 'http://specs.openid.net/auth/2.0/provider')

def xfn(resource):
    return _link(resource, 'http://gmpg.org/xfn/11')

def avatar(resource):
    return _link(resource, 'http://webfinger.net/rel/avatar')


if __name__ == '__main__':
    import sys
    res = finger(sys.argv[1])
    print "Profile:", profile(res)
    print "HCard:  ", hcard(res)
    print "XFN:    ", xfn(res)
    print "OpenID: ", openid(res)
    print "Avatar: ", avatar(res)
