def camel_to_snake(text: str) -> str:
    result = ""
    for letter in text:
        if letter.isupper() and result != "":
            result += "_"
        result += letter.lower()
    return result
