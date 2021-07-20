def ask_yes_no(text: str, default: bool = False) -> bool:
    """Спрашивает в консоле у пользователя 'Yes' или 'No'.

    Args:
        text: Текст, который будет выведен в приведствии.
        default: Значение по умолчанию.

    Returns:
        True - если пользователь ответил 'Yes', False - если пользователь ответил 'No'.
    """
    def generate_prompt():
        answers_prompt = ['y', 'n']
        if default:
            answers_prompt[0] = 'Y'
        else:
            answers_prompt[1] = 'N'

        return f'{text} ({answers_prompt[0]}/{answers_prompt[1]}): '

    yes_value = ('y', 'yes', '1')
    no_value = ('n', 'no', '0')

    prompt = generate_prompt()
    while True:
        s = input(prompt).lower()

        if s in yes_value:
            return True
        elif s in no_value:
            return False
        elif s == '':
            return default
