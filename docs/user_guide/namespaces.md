In version 0.0.10 `lrmtfy` introduced namespaces to give users more flexibility and to make
sharing easier.

Every user has a default namespace that corresponds to their username and a short suffix depending
on the kind of login that you use.

You can see available namespace when you import the catalog. The best way to manage namespaces is 
to start an `ipython` session.

For me the output is the following:
```python title="Importing catalog" linenums="1" hl_lines="3"
In [1]: from lmrtfy.functions import catalog
2022-10-11 16:57:03 [65349] INFO Available namespaces: ['examples', 'orgarten_gh', 'orgarten_gh/shared']
2022-10-11 16:57:04 [65349] INFO Added function: catalog.examples.free_fall_lmrtfy
2022-10-11 16:57:05 [65349] INFO Added function: catalog.orgarten_gh.calc_compound_interest
2022-10-11 16:57:05 [65349] INFO Added function: catalog.orgarten_gh.free_fall_lmrtfy
```

Namespaces available to me are my private one `orgarten_gh` and the example namespace `examples`. 
To use a deployed function inside the namespace I would simply call

```python title="Using a function in a namespace" linenums="1"
catalog.orgarten_gh.<function>(...)
```

If the code editor or IDE of your choice supports auto-completion, the available functions should
be suggested. 

## Create namespaces

You can create new namespaces inside your own user namespace:
```python title="Creating new namespaces" linenums="1"
In [2]: catalog.create_namespace(catalog.orgarten_gh, "shared")
2022-10-11 18:27:27 [58002] INFO {'namespaces': ['orgarten_gh', 
'orgarten_gh/shared']}
```

To add a function inside a namespace you just run `add_function_to_namespace`.

```python title="Add a function to a namespace" linenums="1"
In [3]: catalog.add_function_to_namespace(catalog.orgarten_gh.shared,
   ...: catalog.orgarten_gh.calc_compound_interest)
```

Now you can [share](sharing/sharing.md) the namespace with other users!