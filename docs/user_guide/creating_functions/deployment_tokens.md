If you run lmrtfy with a headless setup (Raspberry Pi, server, google colab, ..) you cannot use
`lmrtfy login` to authenticate. 

To mitigate this issue you can create a deployment token from the catalog. The deployment token
is valid for the function that has been specified.

The following listing creates a token for `<funtion>` in `<namespace>`. This can be any function 
available owned by you.
 
```python title="IPython listing" linenums="1"
In [1]: from lmrtfy.functions import catalog
Out[2]: 

In [2]: catalog.issue_deploy_token(catatlog.<namespace>.<function>)
Out[2]: 
{'token_id': '4HLTgo9bKhaK6kvv2dYA',
 'token': 'LMRTFY...'}
```

The token always starts with `LMRTFY`. The `token_id` is needed to revoke the deployment key when you
don't want to use it anymore. Keep the deployment token secret.

In order to use deployment key you need to set the `LMRTFY_ACCESS_TOKEN` environment variable:
```shell title="Using the deployment token"
$ LMRTFY_ACCESS_TOKEN="LMRTFY..." lmrtfy deploy <script.py> --local --namespace="<namespace>"
```

This way you can use `lmrtfy` on any platform, that does not allow a regular login. `<namespace>` 
is the same namespace that is used in the first listing.

To revoke the deployment key, you just need to do the following:

```python title="Revoke the key" linenums="1"
In [3]: catalog.revoke_token(<token_id>)
Out[3]: True
```

!!! note
    Tokens will be available in the web app.