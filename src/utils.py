def ask_yes_no(text: str, default: bool = False) -> bool:
    yes_value = ('y', 'yes', '1')
    no_value = ('n', 'no', '0')

    value_prompt = ['y', 'n']

    if default:
        value_prompt[0] = 'Y'
    else:
        value_prompt[1] = 'N'

    prompt = f'{text} ({value_prompt[0]}/{value_prompt[1]}) '

    while True:
        s = input(prompt)

        if s in yes_value:
            return True
        elif s in no_value:
            return False
        elif s == '':
            return default
