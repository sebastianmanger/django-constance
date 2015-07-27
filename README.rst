Constance - Dynamic Django settings
===================================

.. image:: https://secure.travis-ci.org/jezdez/django-constance.png
    :alt: Build Status
    :target: http://travis-ci.org/jezdez/django-constance

A Django app for storing dynamic settings in pluggable backends (Redis and
Django model backend built in) with an integration with the Django admin app.

For more information see the documentation at:

http://django-constance.readthedocs.org/

If you have questions or have trouble using the app please file a bug report
at:

https://github.com/jezdez/django-constance/issues


Features
--------

* Add configurable additional fields (merged from ```https://github.com/PetrDlouhy/django-constance```):

.. code-block:: python

    CONSTANCE_ADDITIONAL_FIELDS = {
        'yes_no_select': ['django.forms.fields.ChoiceField', {
            'widget': 'django.forms.Select',
            'choices': (("emotional", _("Emotional")), ("static", _("Static")))
        }],
    }

    CONSTANCE_CONFIG = {
        'MY_SETTINGS_KEY': (42, 'the answer to everything'),
        'MY_SELECT_KEY': ('emotional', 'Select emotional or static', 'yes_no_select'),
    }
