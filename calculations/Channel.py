import random
import copy

class Channel:
    def __init__(self, p):
        """
        p: klaidos tikimybė (error probability).
        """
        self.p = p

    def get_random_value(self):
        """
        Grąžina atsitiktinę reikšmę iš intervalo [0, 1].
        """
        return random.uniform(0, 1)

    def should_distort(self):
        """
        Nustato, ar elementas turėtų būti iškraipytas.
        """
        return self.get_random_value() < self.p

    def distort_element(self, elem):
        """
        Pakeičia 1 į 0 ir 0 į 1.
        """
        return 0 if elem == 1 else 1

    def send(self, c):
        """
        Priima užkoduotą pranešimą `c` ir siunčia jį kanalu su galimu elementų iškraipymu.
        Grąžina iš kanalo išėjusį pranešimą.
        """
        sent = copy.deepcopy(c)  # Giliai kopijuojame masyvą, kad išvengtume nuorodų problemų
        for i in range(len(c)):
            if self.should_distort():
                # print(f"Klaida įterpta į poziciją {i}: {sent[i]} -> {self.distort_element(sent[i])}")
                sent[i] = self.distort_element(sent[i])
        return sent