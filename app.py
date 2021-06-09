from sociolyzer import app

if __name__ == "__main__":
    # threaded to serve multiple users
    app.run(threaded=True)
