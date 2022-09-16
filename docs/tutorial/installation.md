There are two ways to install the `lmrtfy`. We recommend the usage of virtual environments
at the moment due to the frequent updates and changes of lmrtfy.

# Linux and MacOS
We provide a PyPI package for Linux and MacOS which can be installed easily with `pip`:

```shell
$ pip install lmrtfy
```

## Windows
On Windows the `conda` package manager provided by
[miniconda and Anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html)
is the best way to use Python and install Python packages.

Right now, we only support a PyPI package which can be installed with `conda`. If you have `pip` installed
in your conda environment you can directly install from PyPI, otherwise you need to install `pip` first:
```shell
$ conda install pip
$ pip install lmrtfy
```

This way you will always have the most recent release of `lmrtfy`.

# Install from Source
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


