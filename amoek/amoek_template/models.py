# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.pages.models import Page
from mezzanine.core.models import Orderable
from mezzanine.core.fields import FileField

from urllib import unquote
from string import punctuation

# Create your models here.
# coding=utf-8


class Slide(Orderable):
    """
    """
    page = models.ForeignKey(Page, null=True, blank=True, related_name='slides')
    file = FileField(_('File'), max_length=200, upload_to='slides', format='Image')
    description = models.CharField(_('Description'), blank=True, max_length=70)
    link_text = models.CharField(_('Link text'), blank=True, null=True, max_length=70)
    link = models.URLField(_('Link'), blank=True, null=True)
    size_text = models.CharField(
        _('Size'),
        max_length=5,
        choices=(
            ('h1', 'h1'),
            ('h2', 'h2'),
            ('h3', 'h3'),
            ('h4', 'h4'),
            ('h5', 'h5'),
        )
    )
    extra_description = models.TextField(
        blank=True,
        null=True
    )
    resize = models.BooleanField(_('Resize'))

    class Meta:
        verbose_name = _('Slide')
        verbose_name_plural = _('Slides')
        ordering = ['_order']

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        """
        If no description is given when created, create one from the
        file name.
        """
        if not self.id and not self.description:
            name = unquote(self.file.url).split('/')[-1].rsplit('.', 1)[0]
            name = name.replace("'", '')
            name = ''.join([c if c not in punctuation else ' ' for c in name])
            # str.title() doesn't deal with unicode very well.
            # http://bugs.python.org/issue6412
            name = ''.join([s.upper() if i == 0 or name[i - 1] == ' ' else s
                            for i, s in enumerate(name)])
            self.description = name
        super(Slide, self).save(*args, **kwargs)


class ExtraInfo(models.Model):
    """
    Allows for pretty banner images across the top of pages that will cycle
    through each other with a fade effect.
    """
    page = models.OneToOneField(Page, null=True, blank=True, related_name='extra_info')
    description = models.CharField(
        max_length=50
    )

    class Meta:
        verbose_name = _('Extra Info')
        verbose_name_plural = _('Extra Info')
        # ordering = ['_order']

    def __unicode__(self):
        return self.description
        
