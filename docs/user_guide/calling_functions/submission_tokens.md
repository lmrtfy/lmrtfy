If you run lmrtfy with a headless setup (Raspberry Pi, server, google colab, ..) you cannot use
`lmrtfy login` to authenticate.

If you are running a web frontend that calls an LMRTFY function you can use

The following listing creates a token for a `<funtion>` that is available in `<namespace>`. Submit
tokens can be issued for any function that you can call.

```python title="IPython listing" linenums="1"
In [1]: from lmrtfy.functions import catalog
Out[2]: 

In [2]: catalog.issue_submit_token(catatlog.<namespace>.<function>)
Out[2]: 
{'token_id': '4HLTgo9bKhaK6kvv2dYA',
 'token': 'LMRTFY...'}
```

The token always starts with `LMRTFY`. The `token_id` is needed to revoke the deployment key when you
don't want to use it anymore. Keep the deployment token secret.

In order to use deployment key you need to set the `LMRTFY_ACCESS_TOKEN` environment variable:
```shell title="Using the deployment token"
$ LMRTFY_ACCESS_TOKEN="LMRTFY..." ipython
In [1]: from lmrtfy.functions import catalog
Out[1]: ...

In [2]: job = catalog.<namespace>.<function>(...)
```

This way you can use `lmrtfy` on any platform, that does not allow a regular login.

To revoke the submit key, you just need to do the following:

```python title="Revoke the key" linenums="1"
In [3]: catalog.revoke_token(<token_id>)
Out[3]: True
```

If the revocation failed, it will raise an error.

!!! note
    Tokens will be available in the web app.
