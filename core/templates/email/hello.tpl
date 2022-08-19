{% extends "mail_templated/base.tpl" %}

{% block subject %}
account activarions
{% endblock %}

{% block html %}
<strong>{{token}}</strong>
{% endblock %}