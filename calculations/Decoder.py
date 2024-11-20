import numpy as np
from calculations.Converter import Converter


class Decoder:
    def __init__(self):
        self.H = [[1, 1], [1, -1]]  # Hadamardo bazinė matrica

    def decode(self, y, m):
        """
        Dekoduoja vektorių naudodamas Hadamardo transformaciją.
        """
        print(f"Pradinė gauta žinutė: {y}")
        y = self.replace_ones(y)
        print(f"Gauta žinutė po 0 keitimo į -1: {y}")
        vector = self.get_vector_for_decoding(y, m)
        print(f"Vektorius po Hadamardo sandaugų: {vector}")
        position = self.get_largest_absolute_value_position(vector)
        print(f"Didžiausios absoliučios reikšmės pozicija: {position}")
        return self.get_decoded_message(position, m, vector)

    def replace_ones(self, vector):
        """
        Pakeičia 0 į -1 vektoriuje.
        """
        return [-1 if x == 0 else x for x in vector]

    def get_largest_absolute_value_position(self, vector):
        largest = 0
        position = -1

        for i, value in enumerate(vector):
            abs_value = abs(value)
            print(f"Pozicija: {i}, Reikšmė: {value}, Absoliuti reikšmė: {abs_value}")
            if abs_value > largest:
                largest = abs_value
                position = i

        print(f"Didžiausios absoliučios reikšmės pozicija: {position}")
        return position

    def get_decoded_message(self, num, m, vector):
        print(f"Pradinis skaičius: {num}, m: {m}")
        binary = bin(num)[2:].zfill(m)
        print(f"Sugeneruota dvejetainė eilutė: {binary}")

        if vector[num] >= 0:
            binary = "1" + binary
        else:
            binary = "0" + binary

        print(f"Dvejetainė eilutė (su ženklu): {binary}")
        decoded_message = [int(bit) for bit in binary]
        print(f"Dekoduota žinutė: {decoded_message}")
        return decoded_message

    def calculate_kronecker_product(self, matrix1, matrix2):
        """
        Apskaičiuoja Kronekerio sandaugą tarp dviejų matricų.
        """
        rows1, cols1 = len(matrix1), len(matrix1[0])
        rows2, cols2 = len(matrix2), len(matrix2[0])

        result = [[0] * (cols1 * cols2) for _ in range(rows1 * rows2)]

        for i in range(rows1):
            for j in range(cols1):
                for k in range(rows2):
                    for l in range(cols2):
                        result[i * rows2 + k][j * cols2 + l] = matrix1[i][j] * matrix2[k][l]
        return result

    def generate_identity_matrix(self, dimension):
        """
        Sugeneruoja vienetinę matricą nurodyto dydžio.
        """
        return [[1 if i == j else 0 for j in range(dimension)] for i in range(dimension)]

    def get_hadamard_matrix(self, i, m):
        """
        Apskaičiuoja Hadamardo matricą H(i, m).
        """
        identity1 = self.generate_identity_matrix(2 ** (m - i))
        identity2 = self.generate_identity_matrix(2 ** (i - 1))

        temp = self.calculate_kronecker_product(identity1, self.H)
        return self.calculate_kronecker_product(temp, identity2)

    def get_vector_for_decoding(self, vector, m):
        """
        Generuoja dekodavimo vektorių naudojant Hadamardo matricą.
        """
        for i in range(1, m + 1):
            hadamard_matrix = self.get_hadamard_matrix(i, m)
            print(f"Hadamardo matrica H({i}, {m}): {hadamard_matrix}")
            vector = self.multiply_matrix_and_vector(hadamard_matrix, vector)
            print(f"Po Hadamardo sandaugos H({i}, {m}): {vector}")
        return vector

    def multiply_matrix_and_vector(self, matrix, vector):
        """
        Daugina matricą ir vektorių rankiniu būdu.
        """
        rows = len(matrix)
        cols = len(matrix[0])

        result = [0] * rows

        for i in range(rows):
            for j in range(cols):
                result[i] += matrix[i][j] * vector[j]
        return result
    H = np.array([[1, 1], [1, -1]])

    def decode(self, y, m):
        """
        Dekoduoja vektorių naudodamas Hadamardo transformaciją.
        """
        print(f"Pradinė gauta žinutė: {y}")
        y = self.replace_ones(y)
        print(f"Gauta žinutė po 0 keitimo į -1: {y}")
        vector = self.get_vector_for_decoding(y, m)
        print(f"Vektorius po Hadamardo sandaugų: {vector}")
        position = self.get_largest_absolute_value_position(vector)
        print(f"Didžiausios absoliučios reikšmės pozicija: {position}")
        return self.get_decoded_message(position, m, vector)

    def get_error_positions(self, received, sent):
        """
        Nustato klaidų pozicijas tarp gauto ir siųsto vektorių.
        """
        print(f"Gauta žinutė: {received}")
        print(f"Siųsta žinutė: {sent}")

        positions = []
        for i in range(len(received)):
            if received[i] != sent[i]:
                print(f"Klaida rasta pozicijoje {i}: gauta {received[i]}, siųsta {sent[i]}")
                positions.append(i)
        return positions

    def get_largest_absolute_value_position(self, vector):
        largest = 0
        position = -1

        for i, value in enumerate(vector):
            abs_value = abs(value)
            print(f"Pozicija: {i}, Reikšmė: {value}, Absoliuti reikšmė: {abs_value}")
            if abs_value > largest:
                largest = abs_value
                position = i

        print(f"Didžiausios absoliučios reikšmės pozicija: {position}")
        return position

    def replace_ones(self, vector):
        """
        Pakeičia 0 į -1 vektoriuje.
        """
        return [-1 if x == 0 else x for x in vector]

    def get_decoded_message(self, num, m, vector):
        print(f"Pradinis skaičius: {num}, m: {m}")
        binary = Converter.int_to_binary_string(num, m)
        print(f"Sugeneruota dvejetainė eilutė: {binary}")

        if vector[num] >= 0:
            binary = "1" + binary
        else:
            binary = "0" + binary

        print(f"Dvejetainė eilutė (be ženklo): {binary[:-1]}")
        print(f"Dvejetainė eilutė (su ženklu): {binary}")
        decoded_message = Converter.string_to_int_array(binary)
        print(f"Dekoduota žinutė: {decoded_message}")
        return decoded_message

    def calculate_kronecker_product(self, matrix1, matrix2):
        """
        Apskaičiuoja Kronekerio sandaugą tarp dviejų matricų.
        """
        rows1, cols1 = len(matrix1), len(matrix1[0])
        rows2, cols2 = len(matrix2), len(matrix2[0])

        result = [[0] * (cols1 * cols2) for _ in range(rows1 * rows2)]

        for i in range(rows1):
            for j in range(cols1):
                for k in range(rows2):
                    for l in range(cols2):
                        result[i * rows2 + k][j * cols2 + l] = matrix1[i][j] * matrix2[k][l]
        return result

    def generate_identity_matrix(self, dimension):
        """
        Sugeneruoja vienetinę matricą nurodyto dydžio.
        """
        return [[1 if i == j else 0 for j in range(dimension)] for i in range(dimension)]

    def get_hadamard_matrix(self, i, m):
        """
        Apskaičiuoja Hadamardo matricą H(i, m).
        """
        identity1 = self.generate_identity_matrix(2 ** (m - i))
        identity2 = self.generate_identity_matrix(2 ** (i - 1))

        temp = self.calculate_kronecker_product(identity1, self.H)
        return self.calculate_kronecker_product(temp, identity2)

    def get_vector_for_decoding(self, vector, m):
        """
        Generuoja dekodavimo vektorių naudojant Hadamardo matricą.
        """
        for i in range(1, m + 1):
            hadamard_matrix = self.get_hadamard_matrix(i, m)
            print(f"Hadamardo matrica H({i}, {m}): {hadamard_matrix}")
            vector = self.multiply_matrix_and_vector(hadamard_matrix, vector)
            print(f"Po Hadamardo sandaugos H({i}, {m}): {vector}")
        return vector

    def multiply_matrix_and_vector(self, matrix, vector):
        """
        Daugina matricą ir vektorių rankiniu būdu.
        """
        rows = len(matrix)
        cols = len(matrix[0])

        result = [0] * rows

        for i in range(rows):
            for j in range(cols):
                result[i] += matrix[i][j] * vector[j]
        return result
