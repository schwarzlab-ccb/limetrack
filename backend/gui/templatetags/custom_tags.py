from django import template
from ..config.general import (SHOW_BANNER_FOOTER,
                              NAV_BAR_LOGO,
                              SAMPLE_TRACKER_BRAND_NAME)

register = template.Library()


@register.simple_tag
def show_footer():
    return SHOW_BANNER_FOOTER


@register.simple_tag
def logo():
    return NAV_BAR_LOGO


@register.simple_tag
def branding():
    return SAMPLE_TRACKER_BRAND_NAME
