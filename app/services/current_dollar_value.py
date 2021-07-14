import requests
from datetime import date, datetime

# Função que deve ser usada na View -> get_data()


def request_value_dolar(last_price_date):
    return requests.get(
        f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{last_price_date}'&$top=100&$format=json"
    )


def get_valid_date(sub_day, used_date):
    str_year = str(used_date).split("-")[0]
    str_mouth = str(used_date).split("-")[1]
    str_day = str(used_date).split("-")[2]

    str_day = int(str_day) - sub_day

    date_output = "{0}-{1}-{2}".format(str_mouth, str_day, str_year)

    api_bcb = request_value_dolar(date_output)
    api_response = api_bcb.json()["value"]

    sell_rate = api_response[0]['cotacaoVenda']
    new_ptax = {"date": date_output, "sell_rate": str(sell_rate)}
    return new_ptax


def get_date():
    current_date = date.today()
    str_mouth = str(current_date).split("-")[0]
    str_day = str(current_date).split("-")[1]
    str_year = str(current_date).split("-")[2]

    check_fs = current_date.isoweekday()
    if check_fs == 6:
        str_day = int(str_day) - 1

    if check_fs == 7:
        str_day = int(str_day) - 2

    date_output = "{0}-{1}-{2}".format(str_mouth, str_day, str_year)
    return date_output


def get_data(date_input):
    current_date = date.today()
    day_of_date_input = date.fromisoformat(date_input)
    check_fs = current_date.isoweekday()

    input_from_user_fix = fix_date(date_input)
    last_price_date = get_date()

    api_bcb = request_value_dolar(input_from_user_fix)

    if day_of_date_input.isoweekday() == 7:
        valid_date = get_valid_date(2, date_input)
        return valid_date

    if day_of_date_input.isoweekday() == 6:
        valid_date = get_valid_date(1, date_input)
        return valid_date

    if api_bcb.status_code == 500 and check_fs == 1:
        valid_date = get_valid_date(3, last_price_date)
        return valid_date

    if api_bcb.status_code == 500:
        valid_date = get_valid_date(1, last_price_date)
        return valid_date

    api_response = api_bcb.json()["value"]

    try:
        sell_rate = api_response[0]['cotacaoVenda']
    except:
        valid_date = get_valid_date(1, date_input)
        return valid_date

    new_ptax = {"date": input_from_user_fix, "sell_rate": str(sell_rate)}
    return new_ptax


def fix_date(date_input):
    str_year = str(date_input).split("-")[0]
    str_mouth = str(date_input).split("-")[1]
    str_day = str(date_input).split("-")[2]

    date_output = "{0}-{1}-{2}".format(str_mouth, str_day, str_year)
    return date_output
