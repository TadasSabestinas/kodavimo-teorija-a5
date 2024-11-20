from abc import ABC, abstractmethod
from calculations.Channel import Channel
from calculations.Encoder import Encoder
from calculations.Decoder import Decoder

class DataHandler(ABC):
    def __init__(self):
        self.channel = None
        self.encoder = Encoder()
        self.decoder = Decoder()
        self.added_zeros = 0

    @abstractmethod
    def handle_without_encoding(self, input_data, p):
        """
        Abstraktus metodas. Turi būti implementuotas paveldėtose klasėse.
        """
        pass

    @abstractmethod
    def handle_with_encoding(self, input_data, p, m):
        """
        Abstraktus metodas. Turi būti implementuotas paveldėtose klasėse.
        """
        pass

    def divide(self, binary, m):
        """
        Dalina dvejetainę eilutę į dalis, kurių ilgis yra (m+1).
        Prideda trūkstamus nulinius bitus, jei reikia.
        """
        step = m + 1
        divided_arr = [binary[i:i + step] for i in range(0, len(binary), step)]
        remainder = len(binary) % step

        if remainder != 0:
            to_add = step - remainder
            self.added_zeros = to_add
            divided_arr[-1] += '0' * to_add

        return divided_arr
