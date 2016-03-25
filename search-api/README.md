Everything is inside search-api folder

###Setting up virtualenv environment (just the first time)

`virtualenv search-env`

###Activate virtuanenv

`source search-env/bin/activate`

###Deactivate virtualenv

`deactivate`

###Install all required modules from requirements file

`source search-env/bin/activate`
`pip install -r requirements.txt`

###Add new module and update requirements file

`source search-env/bin/activate`
`pip install <module-name>`
`pip freeze > requirements.txt`

