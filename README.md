# User Management System

## Overview

This is a Flask-based user management system that allows administrators to manage users and their associated groups. The application integrates with Amazon S3 for profile picture storage and uses Amazon Cognito for authentication. It also uses Pydantic for data validation and settings management.

## Features

- User authentication with Amazon Cognito
- User profile management
- Group management
- Profile picture upload and display using Amazon S3
- Role-based access control
- Data validation and settings management with Pydantic

## Requirements

- Python 3.13
- Flask
- Flask-WTF
- Flask-Login
- Flask-Migrate
- SQLAlchemy
- Authlib
- boto3
- Pydantic

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/usermgmt.git
    cd usermgmt
    ```
2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
   ```

3. Install the required packages:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
   ```

4. Set up the environment variables:
   Create a .env file in the root directory and add the following environment variables:

    ```sh
    SECRET_KEY=your_secret_key
    SQLALCHEMY_DATABASE_URI=postgresql://username:password@hostname:port/database
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    AWS_ACCESS_KEY_ID=your_aws_access_key_id
    AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
    AWS_REGION=your_aws_region
    S3_BUCKET=your_s3_bucket_name
    COGNITO_USER_POOL_ID=your_cognito_user_pool_id
    COGNITO_APP_CLIENT_ID=your_cognito_app_client_id
    COGNITO_APP_CLIENT_SECRET=your_cognito_app_client_secret
    COGNITO_AUTHORITY=https://cognito-idp.your_region.amazonaws.com/your_user_pool_id
    COGNITO_META_URL=https://cognito-idp.your_region.amazonaws.com/your_user_pool_id/.well-known/openid-configuration
    FLASK_RUN_PORT=5001
    ```
5. Initialize the database:

    ```sh
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

## Running the application

1. Start the development server:
    ```bash
    make run_app
    ```
2. Access the application at `http://localhost:5001`.

## Usage

User Management
  - Create User: Navigate to /users/create to create a new user.
  - Edit User: Navigate to /users/<user_id>/edit to edit an existing user.
  - Delete User: Navigate to /users/<user_id>/delete to delete a user.
  - View User: Navigate to /users/<user_id> to view user details.

Group Management
  - Create Group: Navigate to /groups/create to create a new group.
  - Edit Group: Navigate to /groups/<group_id>/edit to edit an existing group.
  - Delete Group: Navigate to /groups/<group_id>/delete to delete a group.
  - View Group: Navigate to /groups/<group_id> to view group details.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
