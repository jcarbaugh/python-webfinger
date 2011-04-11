from xrd import XRD
import urllib, urllib2

RELS = {
    'avatar': 'http://webfinger.net/rel/avatar',
    'hcard': 'http://microformats.org/profile/hcard',
    'open_id': 'http://specs.openid.net/auth/2.0/provider',
    'portable_contacts': 'http://portablecontacts.net/spec/1.0',
    'profile': 'http://webfinger.net/rel/profile-page',
    'xfn': 'http://gmpg.org/xfn/11',
}

WEBFINGER_TYPES = (
    'lrdd',                                 # current
    'http://lrdd.net/rel/descriptor',       # deprecated on 12/11/2009
    'http://webfinger.net/rel/acct-desc',   # deprecated on 11/26/2009
    'http://webfinger.info/rel/service',    # deprecated on 09/17/2009
)

class WebFingerExpection(Exception):
    pass

class WebFingerResponse(object):
    
    def __init__(self, xrd, insecure):
        self.insecure = insecure
        self._xrd = xrd
    
    def __getattr__(self, name):
        if name in RELS:
            return self._xrd.find_link(RELS[name], attr='href')
        return getattr(self._xrd, name)

class WebFingerClient(object):
    
    def __init__(self, host):
        self._host = host
        self._opener = urllib2.build_opener(urllib2.HTTPRedirectHandler())
        self._opener.addheaders = [('User-agent', 'python-webfinger')]
    
    def _hm_hosts(self, xrd):
        return [e.value for e in xrd.elements if e.name == 'hm:Host']
    
    def xrd(self, url, raw=False):
        conn = self._opener.open(url)
        response = conn.read()
        conn.close()
        return response if raw else XRD.parse(response)
    
    def hostmeta(self, protocol):
        hostmeta_url = "%s://%s/.well-known/host-meta" % (protocol, self._host)
        return self.xrd(hostmeta_url)
    
    def finger(self, username):
        try:
            hm = self.hostmeta('https')
            insecure = False
        except (urllib2.URLError, urllib2.HTTPError):
            hm = self.hostmeta('http')
            insecure = True

        hm_hosts = self._hm_hosts(hm)
        
        if self._host not in hm_hosts:
            raise WebFingerExpection("hostmeta host did not match account host")
                
        template = hm.find_link(WEBFINGER_TYPES, attr='template')
        if not template.startswith('https://'):
            insecure = True
        xrd_url = template.replace('{uri}',
                    urllib.quote_plus('acct:%s@%s' % (username, self._host)))
                    
        data = self.xrd(xrd_url)
        return WebFingerResponse(data, insecure)

def finger(identifier):
    if identifier.startswith('acct:'):
        (acct, identifier) = identifier.split(':', 1)
    (username, host) = identifier.split('@')
    client = WebFingerClient(host)
    return client.finger(username)

# example main method

if __name__ == '__main__':
    import sys
    wf = finger(sys.argv[1])
    print "Avatar: ", wf.avatar
    print "HCard:  ", wf.hcard
    print "OpenID: ", wf.open_id
    print "Profile:", wf.profile
    print "XFN:    ", wf.find_link('http://gmpg.org/xfn/11', attr='href')
    if wf.insecure:
        print "Warning: Data was retrieved over an insecure connection"
