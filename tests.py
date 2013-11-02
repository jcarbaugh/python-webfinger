import unittest
from webfinger import finger, WebFingerClient, WebFingerResponse


class TestHostParsing(unittest.TestCase):

    def setUp(self):
        self.client = WebFingerClient()

    def test_parsing(self):
        host = self.client._parse_host('eric@konklone.com')
        self.assertEqual(host, 'konklone.com')

    def test_official_parsing(self):
        self.client.official = True
        host = self.client._parse_host('konklone@twitter.com')
        self.assertEqual(host, 'twitter.com')

    def test_unofficial_parsing(self):
        self.client.official = False
        host = self.client._parse_host('konklone@twitter.com')
        self.assertEqual(host, 'twitter-webfinger.appspot.com')


class TestWebFingerRequest(unittest.TestCase):

    def setUp(self):
        self.client = WebFingerClient()

    def test_subject(self):
        wf = self.client.finger('acct:eric@konklone.com')
        self.assertEqual(wf.subject, 'acct:eric@konklone.com')


class TestWebFingerResponse(unittest.TestCase):

    def setUp(self):
        jrd = {
            "subject": "acct:eric@konklone.com",
            "properties": {
                "http://schema.org/name": "Eric Mill"
            },
            "links": [
                {
                    "rel": "http://webfinger.net/rel/profile-page",
                    "href": "https://konklone.com"
                },
                {
                    "rel": "http://webfinger.net/rel/avatar",
                    "href": "https://secure.gravatar.com/avatar/ac3399caecce27cb19d381f61124539e.jpg?s=400"
                }
            ]
        }
        self.response = WebFingerResponse(jrd)

    def test_subject(self):
        self.assertEqual(self.response.subject, 'acct:eric@konklone.com')


    def test_rel(self):
        self.assertEqual(self.response.rel('http://webfinger.net/rel/profile-page'), 'https://konklone.com')

    def test_invalid_rel(self):
        self.assertEqual(self.response.rel(''), None)




if __name__ == '__main__':
    unittest.main()
