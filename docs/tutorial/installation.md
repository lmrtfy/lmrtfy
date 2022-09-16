There are two ways to install the lmrtfy tools. We recommend the usage of virtual environments
at the moment due to the frequent updates and changes of lmrtfy.

# Install with pip (recommended)
Use pip to install from PyPI:

`$ pip install lmrtfy`

This way you will always have the most recent release of the lmrtfy tools.

# Install from source
You can also install from git which is the best way to use the nightly features.

Clone the git repository and install manually:
```shell 
$ git clone --branch main https://github.com/lmrtfy/lmrtfy.git
$ cd lmrtfy
$ pip install .
```
The `main` branch is the release branch and should always work with the lmrtfy API. 

Alternatively, you can use the `develop` branch. This should be the most up-to-date branch in the
repository, but things might break. So be careful while using the `develop` branch.



## Install from Source
You can also install LMRTFY from [source](https://github.com/lmrtfy/lmrtfy). This way you can always
try the newest commits from the `main` and `develop` branches.

!!! note
Code from the `main` branch will likely work with current backend. Using code from `develop` is
probably not a good idea, because this will likely break.

If you want to install LMRTFY from source you need to run the following commands:

```shell
$ git clone --branch main https://github.com/lmrtfy/lmrtfy.git
$ cd lmrtfy
$ pip install .
```
