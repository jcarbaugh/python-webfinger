=========
webfinger
=========

A simple Python client implementation of `WebFinger RFC 7033 <http://tools.ietf.org/html/rfc7033>`_.

WebFinger is a discovery protocol that allows you to find information about people or things in a standardized way. See the `spec <http://tools.ietf.org/html/rfc7033>`_ or `webfinger.net <http://webfinger.net>`_ for more information.


Usage
-----

Example::

    >>> from webfinger import finger
    >>> wf = finger('acct:eric@konklone.com')
    >>> wf.subject
    acct:eric@konklone.com
    >>> wf.avatar
    https://secure.gravatar.com/avatar/ac3399caecce27cb19d381f61124539e.jpg?s=400
    >>> wf.profile
    https://konklone.com
    >>> wf.properties.get('http://schema.org/name')
    Eric Mill


WebFinger Response
------------------

The WebFinger response object provides handy properties for easy access and the raw JRD response. Read the `spec for specifics of the JRD response <http://tools.ietf.org/html/rfc7033#section-4.4>`_.


----------
Properties
----------

subject
  The URI of the thing that the response JRD describes.

aliases
  A list of additional URIs that identify the subject.

properties
  A dict of URIs and values that provides information about the subject.

links
  A list of dicts that define external resources for the subject.

jrd
  A dict of the raw JRD response.


-------
Methods
-------

rel(relation, attr='href')
  A convenience method that provides basic access to links. The *relation* parameter is a URI for the desired link. The *attr* parameter is the key of the returned value of the link that matches *relation*. Returns a string if *relation* and *attr* exist, otherwise *None*.

Example::

    >>> wf.rel('http://webfinger.net/rel/avatar')
    https://secure.gravatar.com/avatar/ac3399caecce27cb19d381f61124539e.jpg?s=400


-------------------
Relation Properties
-------------------

The following common link relation types are supported as properties of the response object:

* activity_streams: http://activitystrea.ms/spec/1.0
* avatar: http://webfinger.net/rel/avatar
* hcard: http://microformats.org/profile/hcard
* open_id: http://specs.openid.net/auth/2.0/provider
* opensocial: http://ns.opensocial.org/2008/opensocial/activitystreams
* portable_contacts: http://portablecontacts.net/spec/1.0
* profile: http://webfinger.net/rel/profile-page
* webfist: http://webfist.org/spec/rel
* xfn: http://gmpg.org/xfn/11

Example::

    >>> wf.avatar
    https://secure.gravatar.com/avatar/ac3399caecce27cb19d381f61124539e.jpg?s=400


Unofficial Endpoints
--------------------

While Facebook and Twitter do not officially support WebFinger, the `webfinger-unofficial project <https://github.com/snarfed/webfinger-unofficial>`_ provides a proxy for basic subject information. By default, python-webfinger will attempt to use unoffical the endpoints for facebook.com and twitter.com resource domains. This behavior can be disabled by passing *True* to the *official* parameter::

    >>> wf = finger('acct:konklone@twitter.com', official=True)


Dependencies
------------

* `requests <https://pypi.python.org/pypi/requests>`_


License
-------

python-webfinger is distributed under the `BSD license <http://creativecommons.org/licenses/BSD/>`_.

See LICENSE for the full terms.
