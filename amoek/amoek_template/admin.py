# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf import settings

from mezzanine.pages.models import RichTextPage

from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin
from mezzanine.forms.admin import FormAdmin
from mezzanine.galleries.admin import GalleryAdmin

# from mezzanine_wubook.admin import WubookPageAdmin
from mezzanine_wubook.models import WubookPage, WubookRoomPage
from mezzanine_wubook.admin import WubookRoomPageAdmin as WubookRoomPageAdminOriginal

from amoek_template.models import ExtraInfo

# Register your models here.
# coding=utf-8


#if "cartridge.shop" in settings.INSTALLED_APPS:
#    from cartridge.shop.models import Category
#    from cartridge.shop.admin import CategoryAdmin
#    cartridge = True
#else:
#    cartridge = False

from .models import Slide


"""
We do what we do here instead of just attaching it to PageAdmin because more
things then just pages inherit PageAdmin and if we just inject it into PageAdmin
I've had some very bad things happen. Thus I inject it into each page type
individually in a way that best suits it.
"""


class SlideInline(TabularDynamicInlineAdmin):
    model = Slide


class ExtraInfoInline(admin.TabularInline):
    model = ExtraInfo


class RichTextPageAdmin(PageAdmin):
    inlines = (SlideInline, ExtraInfoInline)


class WubookPageAdmin(PageAdmin):
    inlines = (SlideInline, ExtraInfoInline)
    # fieldsets = deepcopy(PageAdmin.fieldsets) + wubookpage_extra_fields

#class WubookRoomPageAdmin(WubookRoomPageAdminOriginal):
#    inlines = (SlideInline, ExtraInfoInline)


admin.site.unregister(RichTextPage)
admin.site.register(RichTextPage, RichTextPageAdmin)


FormAdmin.inlines += (SlideInline, ExtraInfoInline)
GalleryAdmin.inlines += (SlideInline, ExtraInfoInline)
# WubookPageAdmin.inlines += (SlideInline,)
admin.site.unregister(WubookPage)
admin.site.unregister(WubookRoomPage)
admin.site.register(WubookPage, WubookPageAdmin)
#admin.site.register(WubookRoomPage, WubookRoomPageAdmin)
#if cartridge:
#    class CategoryAdminInline(CategoryAdmin):
#        inlines = (SlideInline,)
#
#    admin.site.unregister(Category)
#    admin.site.register(Category, CategoryAdminInline)


    # admin.site.register(WubookPage, WubookPageAdmin)
