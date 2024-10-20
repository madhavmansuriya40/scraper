import os
import jwt


class User:
    def get_user():
        # Sample JWT token
        token = os.getenv('STATIC_TOKEN')

        try:
            # Decode the token without verifying the signature
            payload = jwt.decode(token, options={"verify_signature": False})

            # Extract the email from the payload
            email = payload.get('email')

            if email:
                return email
            else:
                print("Email not found in the token.")

        except jwt.ExpiredSignatureError:
            print("Token has expired.")
        except jwt.InvalidTokenError:
            print("Invalid token.")
