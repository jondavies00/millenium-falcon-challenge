make pylint-check-core: 
	pylint --output-format=colorized --extension-pkg-whitelist='pydantic' core/falcon_solver

make pylint-check-cli: 
	pylint --output-format=colorized cli\