# Define the environment variables
export FLASK_APP=app
export FLASK_ENV=development

# Target to install dependencies
install:
	pip install -r requirements.txt

# Target to run the Flask app
run_app:
	flask --debug run

# Target to set up the environment and run the app
# setup_and_run: install run_app
