You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] If a TextField has a max_length, it should not be used for validation

**Describe the bug**

Consider this `description` field:

```
    description = models.TextField(
        verbose_name="description", blank=True, max_length=2048
    )
```

According to the [docs](https://docs.djangoproject.com/en/6.0/ref/models/fields/#django.db.models.TextField
), this max_length does not place a restraint on the database: 

> If you specify a max_length attribute, it will be reflected in the [Textarea](https://docs.djangoproject.com/en/6.0/ref/forms/widgets/#django.forms.Textarea) widget of the auto-generated form field. However it is not enforced at the model or database level. Use a [CharField](https://docs.djangoproject.com/en/6.0/ref/models/fields/#django.db.models.CharField) for that.

Now when we query the API for an object with a description longer than 2048, we get:

```
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for NinjaResponseSchema
E       response.description_en
E         String should have at most 2048 characters [type=string_too_long, input_value='012345678901234567890123...78901234567890123456789', input_type=str]
E           For further information visit https://errors.pydantic.dev/2.12/v/string_too_long
```

Note that in the example above, the field is called `description_en`. This is because we use https://github.com/deschler/django-modeltranslation. I don't think that that matters: It's still a TextField. But it might matter, so i mention it here. 

**Versions:**

 - Python version: 3.13
 - Django version: 5.2.12
 - Django-Ninja version: 1.5.3
 - Pydantic version: 2.12.5

