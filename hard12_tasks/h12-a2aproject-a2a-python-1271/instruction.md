You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Feat]: PushNotificationConfig.authentication is ignored; no Authorization header is sent in push notifications

### Is your feature request related to a problem? Please describe.

The A2A protocol spec states that when a client provides a `PushNotificationConfig` with an authentication scheme (e.g. `"schemes": ["Bearer"]`), the A2A server **must authenticate** when sending push notifications to the client’s webhook.
Example config:

```json
"configuration": {
  "pushNotificationConfig": {
    "url": "CALLBACK-URL",
    "token": "secure-client-token-for-task-aaa",
    "authentication": {
      "schemes": ["Bearer"]
    }
  }
}
```

However, the Python implementation (`BasePushNotificationSender`) **completely ignores `authentication`** and sends **no `Authorization` header**.
It only attaches:

```
X-A2A-Notification-Token: <token>
```

This means that webhook endpoints cannot authenticate the caller and cannot follow the security model described in the spec.

This appears to be a **spec compliance gap**: push notification authentication is described by the protocol but not implemented in the Python server.




### Describe the solution you'd like

I would like the Python server to:

* Honor `PushNotificationConfig.authentication`
* Support at least the `"Bearer"` scheme
* Automatically add the appropriate `Authorization` header
* Match the spec examples by sending both:

  * `X-A2A-Notification-Token`
  * `Authorization: Bearer <token_or_jwt>`


### Describe alternatives you've considered

As a workaround, we currently:

* **Subclass `BasePushNotificationSender`**
* Override `_dispatch_notification`
* Inject our own `Authorization: Bearer <jwt>` header

This works, but:

* It duplicates logic that should be part of the framework
* It breaks consistency between Python and other A2A implementations
* It makes spec-compliant webhook security non-standard and harder to maintain

A built-in implementation would make push notification authentication reliable, consistent, and aligned with the A2A spec.

