class Converter:
    RADIX = 2
    NUMBER_OF_BITS = 8

    @staticmethod
    def string_to_int_array(string):
        """
        Konvertuoja įvestą eilutę į sveikųjų skaičių masyvą.
        """
        return [int(ch) for ch in string]

    @staticmethod
    def int_to_binary_string(num, m):
        binary = []
        while num > 0 or len(binary) < m:
            bit = num & 1  # Išskiria mažiausią bitą
            binary.append(str(bit))  # Prideda į pabaigą
            num >>= 1  # Perstumia skaičių
        while len(binary) < m:
            binary.append('0')  # Prideda nulinius bitus į pabaigą
        return ''.join(reversed(binary))  # Grąžina atvirkščią eilutę
