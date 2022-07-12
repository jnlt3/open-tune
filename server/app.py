# main app.py used just as an entry point for the program (and to allow init.py to initialize the needed variables)
from server import app

if __name__ == "__main__":
    app.run(debug=False)
