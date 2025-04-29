from agent.auth_manager import AuthManager

def test_generate_token():
    auth_manager = AuthManager()
    if auth_manager.authenticate_all():
        print("Token generated successfully!")
    else:
        print("Failed to generate token.")

if __name__ == "__main__":
    test_generate_token() 