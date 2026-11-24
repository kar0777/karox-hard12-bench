You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Django Ninja fails with ForeignObject fields: AttributeError 'ForeignObjectRel' object has no attribute 'help_text'

Django Ninja fails to generate ModelSchema when using Django's `ForeignObject` field, which is the recommended workaround for composite primary key relationships in [Django 5.2 documentation](https://docs.djangoproject.com/en/5.2/topics/composite-primary-key/#composite-primary-keys-and-relations).


**Error:**
```
AttributeError: 'ForeignObjectRel' object has no attribute 'help_text'
```

**The models:**

Note:  I'm don't using the  composite primary key in this example.

```python
from django.db import models

class Order(models.Model):
    # ... (fields can be omitted for brevity)
    pass

class Product(models.Model):
    # ... (fields can be omitted for brevity)
    pass

class OrderDetail(models.Model):
    order = models.ForeignObject(
        Order,
        on_delete=models.CASCADE,
        from_fields=["order_id"],
        to_fields=["id"],
        related_name="details"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
```

**The endpoints:**

```python
from ninja import ModelSchema, NinjaAPI
from .models import Order

api = NinjaAPI()


class OrderSchema(ModelSchema):
    class Meta:
        model = Order
        fields = "__all__"


@api.get("/orders", response=list[OrderSchema])
def list_orders(request):
    return Order.objects.all()
```

Django Ninja cannot handle `ForeignObject` fields because `ForeignObjectRel` objects don't have the same attributes as `ForeignKey` relations.

A workaround is to explicitly define the fields in the ModelSchema, but I want to use the `fields = "__all__"`  in the schema definition.

## Reproduction

A minimal reproduction case is available at:  https://github.com/blasferna/django-ninja-foreignobject-issue

To reproduce:
1. Clone the reproduction repository
2. Run `uv sync`
3. Run `uv run manage.py runserver`

The error occurs immediately when Django tries to import the API endpoints.


## Versions:

 - Python version: 3.12
 - Django version: 5.2.5
 - Django-Ninja version: 1.4.3
 - Pydantic version: 2.11.7


