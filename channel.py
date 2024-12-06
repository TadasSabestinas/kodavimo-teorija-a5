import random

class Channel:
    def __init__(self, p):
        self.p = p

    def check_if_should_distort(self):
        #Patikrina ar elementas turetu būti iskraipytas pagal klaidos tikimybe
        return random.uniform(0, 1) < self.p

    def distort_number(self, number):
        #Pakeiciamas elementas i priesinga
        #Parametrai:
        #elem - pradine reiksme (0 arba 1).
        #Grazina pakeista reikšme.

        return 0 if number == 1 else 1

    def send(self, c):
        #Simuliuoja pranesimo siuntima per kanala su klaidomis.
        #Parametrai:
        #c - uzkoduotas pranesimas (vektorius).
        #Gražina pranešima su galimais iskraipymais.

        sent = c[:]  #pradinio pranešimo kopija.
        for i in range(len(c)):
            if self.check_if_should_distort():
                sent[i] = self.distort_number(sent[i])  #elementas iskraipomas.
        return sent
