=========
webfinger
=========

Usage
=====

Example::

	from webfinger import finger

	wf = finger('user@host.com')
	print wf.profile
	print wf.hcard

The following relation types are supported:

* activity_streams: http://activitystrea.ms/spec/1.0
* avatar: http://webfinger.net/rel/avatar
* hcard: http://microformats.org/profile/hcard
* open_id: http://specs.openid.net/auth/2.0/provider
* opensocial: http://ns.opensocial.org/2008/opensocial/activitystreams
* portable_contacts: http://portablecontacts.net/spec/1.0
* profile: http://webfinger.net/rel/profile-page
* xfn: http://gmpg.org/xfn/11

Other relation types can be accessed directly from the XRD document.::

	print wf.find_link('http://example.com/example/spec', attr='href')

Dependencies
============

* `python-rd <http://github.com/jcarbaugh/python-rd>`_

License
=======

python-webfinger is distributed under the `BSD license <http://creativecommons.org/licenses/BSD/>`_.

See LICENSE for the full terms of the BSD license.
