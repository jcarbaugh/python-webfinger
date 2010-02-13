================
python-webfinger
================

Usage
=====

Example::

	from pywebfinger import finger
	
	wf = finger('user@host.com')
	print wf.profile
	print wf.hcard

The following relation types are supported:

* avatar: http://webfinger.net/rel/avatar
* hcard: http://microformats.org/profile/hcard
* open_id: http://specs.openid.net/auth/2.0/provider
* portable_contacts: http://portablecontacts.net/spec/1.0
* profile: http://webfinger.net/rel/profile-page
* xfn: http://gmpg.org/xfn/11

Other relation types can be accessed directly from the XRD document.::

	print wf.find_link('http://example.com/example/spec', attr='href')

Dependencies
============

* `python-xrd <http://github.com/jcarbaugh/python-xrd>`_
* iso8601 (required by python-xrd)

License
=======

python-webfinger is distributed under the `BSD license <http://creativecommons.org/licenses/BSD/>`_.

See LICENSE for the full terms of the BSD license.