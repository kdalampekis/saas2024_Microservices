# your_project/pipeline.py

from authenticationService.views import create_user_credit_balance

def create_user_credit_balance_pipeline(backend, user, response, *args, **kwargs):
    if user:
        status_code, response_text = create_user_credit_balance(user.id)
        if status_code != 201:
            print(f"Failed to create user credit balance for user {user.id}: {response_text}")
        else:
            print(f"User credit balance created for user {user.id}: {response_text}")
