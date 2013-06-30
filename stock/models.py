from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now


class Item(models.Model):

    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(max_length=64, unique=True, editable=False)
    description = models.TextField(_("Description"), blank=True)
    photo = models.ImageField(_("Photo"), upload_to='p/', null=True, blank=True)
    pieces = models.PositiveIntegerField(_("Pieces"), default=0, editable=False)

    def save(self, **kwargs):
        self.slug = slugify(self.name)[:64]
        super(Item, self).save(**kwargs)
        

    def __unicode__(self):
        return u"%s: %d" % (self.name, self.pieces)

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")


TYPE_CHOICES = (
    ("a", _("Income")),
    ("r", _("Issue")),
    ("n", _("No-ops"))
)


class Operation(models.Model):

    user = models.ForeignKey(User, verbose_name=_("Processed by"))
    item = models.ForeignKey(Item, verbose_name=_("Item"))
    type = models.CharField(_("Operation type"), max_length='1', db_index=True, choices=TYPE_CHOICES)
    pieces = models.PositiveIntegerField(_("Pieces"), default=0)
    attachment = models.FileField(_("Document"), upload_to="a/", null=True, blank=True)
    ts = models.DateTimeField(_("Processed at"), editable=False)

    def save(self, **kwargs):
        self.ts = now()
        super(Operation, self).save(**kwargs)

    class Meta:
        verbose_name = _("Operation")
        verbose_name_plural = _("Operations")


@receiver(post_save, sender=Operation)
def update_item(sender, **kwargs):
    op = kwargs.pop("instance")

    # TODO: avoid negative pieces in stock
    if op.type == "a":
        op.item.pieces += op.pieces
        op.item.save(force_update=True)
    elif op.type == "r":
        op.item.pieces -= op.pieces
        op.item.save(force_update=True)
