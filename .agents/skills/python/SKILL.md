---
name: python
description: Guidelines and constraints when using Python for development
---

### Guidelines for running Python when a virtualenv is active
  - look for a file ```.python-version``` in the project folder. This defines the name of which pyenv virtual environment should be active.
 - check for the presence of environment variable ```PYENV_VIRTUAL_ENV```. If this variable is not present, attempt to activate the environment:
 ```
  pyenv activate
```

 - if the environment cannot be started, or if the `.python-version` file does not contain the name of the project folder, **stop** and notify the operator.

### Guidelines for running Python when a virtualenv is not active and no virtualenv folder (.venv) is present
 - If a Python virtual environment is not active when a shell is opened in the project folder,
   create it with pyenv using the project folder name as the name of the virtualenv, create the `.python-version` file,
   and activate it. For example:
```
 pyenv virtualenv spd-analysis
 echo "spd-analysis" > .python-version
 pyenv activate
```
 - If a `requirements.txt` file is present in the project folder, after the virtual environment is active, install the dependencies:

```
pip install -r requirements.txt
```

### Guidelines for running Python and installing dependencies when a virtualenv folder (.venv) is present

 - Execute only the python executable from the 'bin' folder of the virtualenv.

 - When dependencies are required, install them using ```.venv/bin/python -m pip```
 
 - Always use the workspace virtualenv to install required dependencies.
 
 ### Updating requirements.txt

  - requirements for future pip installs (e.g. after retrieving from repository sources) in general should only require equal or greater versions rather than exact versions, potentially allowing use of libraries already installed.
 ```
  pip freeze | sed -i 's/==/>=/' > requirements.txt
 ```


