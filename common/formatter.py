def format_number_with_commas(number):
    """
    주어진 숫자를 천 단위로 ','를 찍어서 문자열로 반환합니다.
    """
    if isinstance(number, (int, float)):
        return f"{number:,}"
    else:
        raise ValueError("숫자 형식의 값만 입력 가능합니다.")

def remove_comma_from_number(string_number):
    return int(string_number.replace(",",""))