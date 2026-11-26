You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] Django's override_settings does not work for Ninja settings

**Describe the bug**
It seems I cannot use Django's `override_settings` for the `NINJA_NUM_PROXIES` setting.

Specifically, the patched setting **does not** work in this case.
```
@override_settings(NINJA_NUM_PROXIES=3)
@override_settings(NUM_PROXIES=3)
def test_throttle_proxied(self):
```

But this **does** work:
```
@patch("ninja.conf.settings.NUM_PROXIES", 3)
def test_throttle_proxied(self):
```

From what I can understand, for some reason Ninja has its own config that is separate but related(?) to the underlying Django config. It seems to break this standard Django settings patching annotation.

**Expected behaviour**

Patching the settings of third-party Django dependencies usually works fine for me, e.g. I use `@override_settings(AXES_ENABLED=False)` in many of my tests. 

I had a look at how axes handles its application settings. It looks different:
```
from django.conf import settings
settings.AXES_ENABLED = getattr(settings, "AXES_ENABLED", True)
```

For this, it seems to just use the default global settings and sets the default only if the user has not set the setting in their own `settings.py` file.

**Versions (please complete the following information):**
 - Python version: 3.12
 - Django version: 5.2.11
 - Django-Ninja version: 1.5.1
 - Pydantic version: 2.11.5

