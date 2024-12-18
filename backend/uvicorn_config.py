from uvicorn import Config, Server

config = Config(
    app="main:app",
    reload=True,
    reload_excludes=["site-packages/*", "*.pyc", "__pycache__"],
)
server = Server(config)
server.run()
