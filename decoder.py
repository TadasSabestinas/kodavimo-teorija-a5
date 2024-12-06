class Decoder:
    def __init__(self):
        #sukuriam bazine Hadamardo matrica.
        self.H = [[1, 1], [1, -1]]

    def replace_ones(self, vector):
        #Pakeicia visas 0 reikšmes i -1.
        #Parametrai:
        #vector - pradine zinute (vektorius).
        #grazina modifikuota vektoriu (0 pakeisti i -1).

        return [-1 if x == 0 else x for x in vector]

    def find_largest_absolute_value_position(self, vector):
        #Randa didziausios absoliucios reikšmes pozicija vektoriuje.
        #Parametrai:
        #vector - apskaiciuotas dekodavimo vektorius.
        #Grazina didziausios absoliucios reiksmes pozicija.

        largest = 0
        position = -1

        for i, value in enumerate(vector):
            abs_value = abs(value)  #skaiciuojama absoliuti reiksme.
            print(f"Pozicija: {i}, Reikšmė: {value}, Absoliuti reikšmė: {abs_value}")
            if abs_value > largest:
                largest = abs_value
                position = i

        print(f"Didžiausios absoliučios reikšmės pozicija: {position}")
        return position

    def calculate_kronecker_product(self, matrix1, matrix2):
        #apskaiciuoja dvieju matricu Kronekerio sandauga.
        #Parametrai:
        #matrix1 - pirmoji matrica.
        #matrix2 - antroji matrica.
        #grazina Kronekerio sandaugos matrica.

        rows1, cols1 = len(matrix1), len(matrix1[0])
        rows2, cols2 = len(matrix2), len(matrix2[0])

        result = [[0] * (cols1 * cols2) for _ in range(rows1 * rows2)] #sukuriam tuscia matricu rezultata

        for i in range(rows1):
            for j in range(cols1):
                for k in range(rows2):
                    for l in range(cols2):
                        #skaiciuojama kiekviena sandaugos reiksme.
                        result[i * rows2 + k][j * cols2 + l] = matrix1[i][j] * matrix2[k][l]
        return result

    def generate_identity_matrix(self, size):
        #Sugeneruoja vienetine matrica nurodyto dydzio.
        #Parametrai:
        #size - vienetines matricos dydis.
        #grazina vienetine matrica.

        return [[1 if i == j else 0 for j in range(size)] for i in range(size)]

    def hadamard_matrix(self, i, m):
        #Sugeneruoja Hadamardo matrica H(i, m).
        #Parametrai:
        #i - dabartinis matricos lygis.
        #m - kodo ilgio parametras.
        #Grazina Hadamardo matrica H(i, m).

        identity1 = self.generate_identity_matrix(2 ** (m - i))
        identity2 = self.generate_identity_matrix(2 ** (i - 1))

        temp = self.calculate_kronecker_product(identity1, self.H)  #Kronekerio sandauga su bazine Hadamardo matrica.
        return self.calculate_kronecker_product(temp, identity2)

    def calculate_vector_for_decoding(self, vector, m):
        #apskaiciuoja vektoriu dekodavimui naudojant Hadamardo matrica.
        #Parametrai:
        #vector - gautas pranesimo vektorius
        #m - kodo ilgio parametras
        #Grazina dekodavimo vektoriu

        for i in range(1, m + 1):
            hadamard_matrix = self.hadamard_matrix(i, m)  #Sugeneruojama Hadamardo matrica
            print(f"Hadamardo matrica H({i}, {m}): {hadamard_matrix}")
            vector = self.multiply_matrix_and_vector(hadamard_matrix, vector)  #Matricos ir vektoriaus sandauga
            print(f"Po Hadamardo sandaugos H({i}, {m}): {vector}")
        return vector

    def multiply_matrix_and_vector(self, matrix, vector):
        #Daugina matrica su vektoriumi skaliariniu būdu.
        #Parametrai:
        #matrix - Hadamardo matrica.
        #vector - gautas vektorius.
        #Grazina sandaugos vektoriu.

        rows = len(matrix)
        cols = len(matrix[0])

        result = [0] * rows

        for i in range(rows):
            for j in range(cols):
                result[i] += matrix[i][j] * vector[j]
        return result

    def retrieve_error_positions(self, received, sent):
        #nustato klaidu pozicijas tarp gauto ir siusto vektoriaus
        #Parametrai:
        #received - gautas pranesimas (vektorius).
        #sent - siustas pranesimas (vektorius).
        #Grazina klaidu poziciju sarasa.

        positions = []
        for i in range(len(received)):
            if received[i] != sent[i]:
                print(f"Klaida rasta pozicijoje {i}: gauta {received[i]}, siųsta {sent[i]}")
                positions.append(i)
        return positions

    def convert_absolute_error_position_to_binary_string(self, num, m):
        #konvertuoja sveikaji sk i m bitų dvejetaine eilute.
        #Parametrai:
        #num - sveikasis skaicius, kuris bus konvertuotas.
        #m - bitų ilgis.
        #Grazina dvejetaine eilute.

        binary_builder = []
        while num > 0 or len(binary_builder) < m:
            bit = num & 1 #paima maziausiai reiksminga bita
            binary_builder.append(str(bit))
            num >>= 1

        while len(binary_builder) < m:
            binary_builder.append('0')

        return ''.join(binary_builder)

    def string_to_int_array(self, string):
        #Konvertuoja dvejetaine eilute i sveikuju skaiciu masyva.
        #Parametrai:
        #string - dvejetaine eilute.
        #Grazina sveikuju skaiciu masyva.

        return [int(ch) for ch in string]
    
    def decode(self, y, m):
        #Dekoduoja pranesima naudodamas greitaja Hadamardo transformacija.
        #Parametrai:
        #y - gautas pranesimo vektorius is kanalo.
        #m - kodo ilgio parametras.
        #Grazina dekoduota pranesima (vektoria).

        print(f"Pradinė gauta žinutė: {y}")
        y = self.replace_ones(y)  #Pakeicia 0 reiksmes i -1.
        print(f"Gauta žinutė po 0 keitimo į -1: {y}")
        vector = self.calculate_vector_for_decoding(y, m)  #apskaiciuoja dekodavimo vektoriu
        print(f"Vektorius po Hadamardo sandaugų: {vector}")
        position = self.find_largest_absolute_value_position(vector)  #randa didziausia reiksme
        print(f"Didžiausios absoliučios reikšmės pozicija: {position}")
        return self.decode_message(position, m, vector)  #grazina dekoduota pranesima.

    def decode_message(self, num, m, vector):
        #Sugeneruoja dekoduota zinute is Hadamardo dekodavimo pozicijos.
        # Parametrai:
        # num - didziausios reiksmes pozicija Hadamardo rezultate.
        # m - kodo ilgio parametras.
        # vector - Hadamardo transformuotas vektorius.
        # Grazina dekoduota zinute kaip vektoriu.

        binary = self.convert_absolute_error_position_to_binary_string(num, m)  #konvertuojama i dvejetaine eilute.
        print(f"Sugeneruota dvejetainė eilutė: {binary}")

        if vector[num] >= 0:
            binary = "1" + binary  #pridedama 1, jei reiksme teigiama.
        else:
            binary = "0" + binary 

        decoded_message = self.string_to_int_array(binary)  #konvertuojama i sveikuju skaiciu masyva.
        print(f"Dekoduota žinutė: {decoded_message}")
        return decoded_message
