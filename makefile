# Define the environment variables
export FLASK_APP=app

# Target to install dependencies
install:
	pip install -r requirements.txt

# Target to run the Flask app
run_app:
	FLASK_ENV=development flask run

# Target to set up the environment and run the app
# setup_and_run: install run_app
