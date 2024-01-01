from django.db import models

PRODUCT_TYPE = (
    ('default', 'Default'),
)

PRODUCT_STATUS = (
    ('activated', 'Activated'),
    ('disabled', 'Disabled'),
)

class Product(models.Model):
    id = models.CharField(max_length=24, primary_key=True)
    code = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    subhead = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=PRODUCT_TYPE, default='default')
    image = models.URLField(null=True, blank=True)
    thumbnail = models.URLField(null=True, blank=True)
    order = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    status = models.CharField(max_length=50, choices=PRODUCT_STATUS, default='activated')
    versionKey = models.IntegerField(default=0)

    # Auto-set the field on creation and update.
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    createdBy = models.TextField(null=True, blank=True)
    updatedBy = models.TextField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        if '__v' in kwargs:
            kwargs['versionKey'] = kwargs.pop('__v')
        if '_id' in kwargs:
            kwargs['id'] = kwargs.pop('_id')
        super(Product, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return f"{self.code} - {self.title}"

    def to_dict(self):
        return {
            "code": self.code,
            "title": self.title,
            "subhead": self.subhead,
            "description": self.description,
            "type": self.type,
            "image": self.image,
            "thumbnail": self.thumbnail,
            "order": self.order,
            "price": float(self.price),
            "stock": self.stock,
            "status": self.status,
        }
