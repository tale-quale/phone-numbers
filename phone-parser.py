from bs4 import BeautifulSoup
import requests
import re


# Is valid russian phone number?
def is_valid_number(number):
    if number[:3] in area_codes:
        return True
    elif number[:4] in area_codes:
        return True
    elif number[:5] in area_codes:
        return True
    else:
        return False

def get_valid_numbers(phones):
    valid_phones = []
    for i in range(len(phones)):
        if is_valid_number(phones[i]):
            valid_phones.append(phones[i])

    return valid_phones

def get_area_codes(filename='area_codes.txt'):
    with open(filename, 'r') as f:
        area_codes = f.readlines()
    #map(lambda s: s.replace('\n', ''), area_codes)
    area_codes = [elem.rstrip() for elem in area_codes]

    return area_codes

def main():
    global area_codes
    area_codes = get_area_codes()

    pattern = r'((\+7|8|7)[- ]*)((\(?[- ]*\d{3,5}[- ]*\)?)?([- ]*\d){5,7}|\d\d[- ]*\d\d[- ]*\)?([- ]*\d){6})'
    pattern = r'((\+7|8|7)[- _]*)?((\(?[- _]*\d{3,5}[- _]*\)?)?([- _]*\d){5,7}|\d\d[- _]*\d\d[- _]*\)?([- _]*\d){6})'
    urls = ['https://hands.ru/company/about/',
            'https://repetitors.info/',
            'https://www.atol.ru/contacts/kontakty-atol/',
            'https://kraska.ru/kontaktyi']
    url = urls[0]
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    #with open('output.txt', 'w') as f:
    #    f.write(soup.get_text())
    phones = re.findall(pattern, soup.get_text())
    #print(phones)
    phones = [x[2] for x in phones if x[3]] # get raw phone numbers without leading +7|8
    # normalize data in phones
    for i in range(len(phones)):
        phones[i] = re.sub(r'[- \(\)]', '', phones[i])

    phones = [number for number in phones if len(number) == 10 or len(number) == 7] # validate number's length
    phones = get_valid_numbers(phones) # check area code in raw numbers
    phones_set = set(phones) # remove duplicates
    for elem in phones_set:
        prefix = '8'
        if len(elem) == 7: # if number without area code it is from Moscow
            prefix += '495'
        print(f'{prefix}{elem}')


if __name__ == '__main__':
    main()