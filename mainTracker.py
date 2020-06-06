#!/usr/bin/python3
# -*- coding: utf-8; mode: python-*-

# author: Sergio Martín-Delgado Gutiérrez
# Date: may 2020

import requests
from bs4 import BeautifulSoup
import smtplib
import time

import cfg


def get_url():
    URL = 'https://www.amazon.es/Nuevo-Apple-pulgadas-Wi-Fi-128-GB/dp/' \
          'B0863RPSHB/ref=sr_1_4?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=' \
          '1&keywords=IPAD+PRO&qid=1591351476&sr=8-4'

    return URL


def get_headers():
    headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}

    return headers


def get_product():
    title = None
    while title is None:
        page = requests.get(get_url(), headers=get_headers())

        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find(id="productTitle")
        price = soup.find(id="priceblock_ourprice")

    product_list = [title.get_text(), price.get_text()]
    return product_list


def check_price(server, less_price):

    product_list = get_product()

    title = product_list[0]
    price = product_list[1]
    converted_price = price[0:str(price).find(" ")]
    converted_price = float(converted_price.replace(",", "."))

    if converted_price < 1500 and converted_price < less_price:
        send_mail(server)

    print(f"Price now: {converted_price} €")
    print(title.strip())
    print(f"less price: {less_price} €\n\n")

    return converted_price


def create_server():
    print("Starting server...")

    server = smtplib.SMTP(cfg.SMTP_SERVER, cfg.SMTP_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()

    print("Server start!\n")

    return server


def send_mail(server):

    server.login(cfg.MAIL_FROM, cfg.PASSWORD)

    subject = 'Amazon: iPad Pro Price fell down!'
    body = f'Check the Amazon link: {get_url()}'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        cfg.MAIL_FROM,
        cfg.MAIL_TO,
        msg
    )

    print('HEY EMAIL HAS BEEN SENT!')


def main():
    try:
        server = create_server()
        price = 1500
        while True:
            price = check_price(server, price)
            time.sleep(10)

    except KeyboardInterrupt:
        server.quit()
        print('KeyboardInterrupt')


if __name__ == "__main__":
    main()
