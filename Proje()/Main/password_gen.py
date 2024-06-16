import random

def randompassword():
    kucuk_harfler = "".join(chr(s) for s in range(ord('a'), ord('z') + 1))
    buyuk_harfler = "".join(chr(s) for s in range(ord('A'), ord('Z') + 1))
    sayilar = "0123456789"
    sifre = ""
    liste = [kucuk_harfler, sayilar, buyuk_harfler, kucuk_harfler]

    for i in range(15):
        sifre += random.choice(liste[i % 4])
    
    return sifre


