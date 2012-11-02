import logging
import urllib
import requests

import rd

__version__ = '0.2'

RELS = {
    'activity_streams': 'http://activitystrea.ms/spec/1.0',
    'avatar': 'http://webfinger.net/rel/avatar',
    'hcard': 'http://microformats.org/profile/hcard',
    'open_id': 'http://specs.openid.net/auth/2.0/provider',
    'opensocial': 'http://ns.opensocial.org/2008/opensocial/activitystreams',
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

UNOFFICIAL_ENDPOINTS = {
    'facebook.com': 'facebook-webfinger.appspot.com',
    'twitter.com': 'twitter-webfinger.appspot.com',
}

logger = logging.getLogger("webfinger")


class WebFingerException(Exception):
    pass


class WebFingerResponse(object):
    """ Response that wraps an RD object. This class provides a `secure`
        parameter to indicate whether the response was returned via HTTP or
        HTTPS. It also provides attribute-style access to links for specific
        rels, responding with the href attribute of the matched element.
    """

    def __init__(self, rd, secure=False):
        self.secure = secure
        self.rd = rd

    def __getattr__(self, name):
        if name in RELS:
            return self.rd.find_link(RELS[name], attr='href')
        return getattr(self.rd, name)


class WebFingerClient(object):

    def __init__(self, host, timeout=None, official=False):
        self._host = host
        self._official = official
        self._session = requests.session(
            timeout=timeout,
            headers={'User-Agent': 'python-webfinger'})

    def rd(self, url, raw=False):
        """ Load resource at given URL and attempt to parse either XRD or JRD
            based on HTTP response Content-Type header.
        """
        resp = self._session.get(url)
        content = resp.content
        return content if raw else rd.loads(content, resp.headers.get('Content-Type'))

    def hostmeta(self, secure=True):
        """ Load host-meta resource from WebFinger provider.
            Defaults to a secure (SSL) connection unless secure=False.
        """

        protocol = "https" if secure else "http"

        # use unofficial endpoint, if enabled
        if not self._official and self._host in UNOFFICIAL_ENDPOINTS:
            host = UNOFFICIAL_ENDPOINTS[self._host]
        else:
            host = self._host

        # create full host-meta URL
        hostmeta_url = "%s://%s/.well-known/host-meta" % (protocol, host)

        # attempt to load from host-meta.json resource
        resp = self._session.get("%s.json" % hostmeta_url)

        if resp.status_code == 404:
            # on failure, load from RFC 6415 host-meta resource
            resp = self._session.get(hostmeta_url, headers={"Accept": "application/json"})          # fall back to XRD

        if resp.status_code != 200:
            # raise error if request was not successful
            raise WebFingerException("host-meta not found")

        # load XRD or JRD based on HTTP response Content-Type header
        return rd.loads(resp.content, resp.headers.get('Content-Type'))

    def finger(self, username, rel=None):
        """ Perform a WebFinger query based on the given username.
            The `rel` parameter, if specified, will be passed to the provider,
            but be aware that providers are not required to implement the
            rel filter.
        """

        try:
            hm = self.hostmeta()               # attempt SSL host-meta retrieval
        except (requests.RequestException, requests.HTTPError):
            hm = self.hostmeta(secure=False)   # on failure, attempt non-SSL

        if hm is None:
            raise WebFingerException("Unable to load or parse host-meta")

        # find template for LRDD document
        template = hm.find_link(WEBFINGER_TYPES, attr='template')
        secure = template.startswith('https://')

        rd_url = template.replace('{uri}',
                    urllib.quote_plus('acct:%s@%s' % (username, self._host)))

        data = self.rd(rd_url)
        return WebFingerResponse(data, secure)


def finger(identifier, rel=None, timeout=None, official=False):
    """ Shortcut method for invoking WebFingerClient.
    """

    if ":" in identifier:
        (scheme, identifier) = identifier.split(':', 1)

    (username, host) = identifier.split('@')

    client = WebFingerClient(host, timeout=timeout, official=official)
    return client.finger(username, rel=rel)


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description="Simple webfinger client.")
    parser.add_argument("acct", metavar="URI", help="account URI")
    parser.add_argument("-d", "--debug", dest="debug", action="store_true", help="print debug logging output to console")
    parser.add_argument("-r", "--rel", metavar="REL", dest="rel", help="desired relation")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    wf = finger(args.acct, rel=args.rel)

    if args.rel:

        link = wf.find_link(args.rel)

        if link is None:
            print "*** Link not found for rel=%s" % args.rel

        print "%s:\n\t%s" % (link.rel, link.href)

    else:

        print "Activity Streams:  ", wf.activity_streams
        print "Avatar:            ", wf.avatar
        print "HCard:             ", wf.hcard
        print "OpenID:            ", wf.open_id
        print "Open Social:       ", wf.opensocial
        print "Portable Contacts: ", wf.portable_contacts
        print "Profile:           ", wf.profile
        print "XFN:               ", wf.find_link("http://gmpg.org/xfn/11", attr="href")

    if not wf.secure:
        print "\n*** Warning: Data was retrieved over an insecure connection"
