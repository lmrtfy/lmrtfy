You can share your functions with others, and they can simply use it from their code just as simply 
as you can.

All you need is the email address of the person you want to share with. We take care of the rest. 

Sharing is implemented on a [namespace level](../namespaces.md).

# Sharing via code

Using code is the easiest way to share a namespace. There are 3 steps to share a function:

1. Create a namespace that you want to share
2. Add the function you want to share to the namespace
3. Share the namespace via e-mail

In code it looks just like this:

```python title="Sharing a function" linenums="1"
from lmrtfy.functions import catalog

catalog.create_namespace(catalog.<user_namespace>, "new_namespace")

catalog.add_function_to_namespace(catalog.<user_namespace>.new_namespace, 
                                  catatlog.<user_namespace>.<function>)

catalog.share_namespace(catalog.<user_namespace>.new_namespace, 
                        "someone@somewhere.com")
```

`<user_namespace>` is the namespace that is bound to your user and is `<username>_a0` if you 
use a username/password combination for your account. If you use a social login the username will
be taken from there. To ensure uniqueness we add a suffix to the username to create the namespace:

* for Auth0 (username/password): `<username>_a0`
* for GitHub: `<username>_gh`
* for Google: `<username>_gl`

`<function>` is any function that is available in your catalog and owned by you.

The output of th script above is an invite ID. The invite is sent via email to the specified recipient.
The invite is not bound to this email address. If the invitee uses another email for LMRTFY they can
just login with their regular account to accept the invite. 

Alternatively, the invitation can be accepted via code as well:

```python title="Accepting an invite in code"
catalog.accept_invite("<invite_id>")
```


