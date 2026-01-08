def get_response(user_input: str):
    user_input = user_input.lower()

    if user_input == 'hello':
        return("Hello!")
    elif user_input == 'bye':
        return("Goodbye!")
    else:
        return("peck!")
