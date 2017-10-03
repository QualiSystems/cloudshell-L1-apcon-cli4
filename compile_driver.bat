pyinstaller --onefile driver.spec
copy datamodel\*.xml dist /Y
copy apcon_cli4_runtime_configuration.json dist /Y
