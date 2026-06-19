from nicegui import ui

ui.label('Hello World from NiceGUI!')

# Run NiceGUI bound to 0.0.0.0 and port 8080 (as expected by Docker Compose)
# show=False prevents NiceGUI from trying to open a browser window inside the Docker container
ui.run(host='0.0.0.0', port=8080, show=False)
