class Encoder:
    def __init__(self):
        pass

    def combine_two_matrix_horizontally(self, matrix1, matrix2):
        # Horizontaliai sujungia dvi matricas.
        # Parametrai:
        # matrix1 - pirmoji matrica.
        # matrix2 - antroji matrica.
        # Grąžina horizontaliai sujungtą matricą.

        return [row1 + row2 for row1, row2 in zip(matrix1, matrix2)]

    def combine_two_matrix_vertically(self, matrix1, matrix2):
        # Vertikaliai sujungia dvi matricas.
        # Parametrai:
        # matrix1 - viršutinė matrica.
        # matrix2 - apatinė matrica.
        # Grąžina vertikaliai sujungtą matricą.

        return matrix1 + matrix2

    def generate_last_row(self, m, num):
        # Sugeneruoja pusę paskutinės eilutės su 1 arba 0 reikšmėmis.
        # Parametrai:
        # m - kodo ilgio parametras.
        # num - reikšmė (1 arba 0).
        # Grąžina matricą su viena eilute.

        length = 2 ** (m - 1)  # Apskaičiuojamas eilutės ilgis.
        return [[num] * length]

    def multiply_matrix_and_vector(self, matrix, vector):
        # Padaugina matricą ir vektorių mod 2.
        # Parametrai:
        # matrix - generatoriaus matrica.
        # vector - vektorius, kuris bus užkoduotas.
        # Grąžina užkoduotą vektorių.

        result = []
        for row in zip(*matrix): #teilutės tampa stulpeliais, o stulpeliai eilutėmis, kad butu lengva iteruot
            #padaugina generatoriaus matrica is pranesimo vektoriaus ir grazina uzkoduota vektoriu moduliu 2
            value = sum(v * r for v, r in zip(vector, row)) % 2
            result.append(value)
        return result
    
    def generate_matrix(self, r, m):
        #sugeneruoja RM(r, m) generatorine matrica rekursyviai.
        #Parametrai:
        #r - kodo eile.
        #m - kodo ilgis.
        #grazina sugeneruota RM(r, m) generatoriaus matrica.

        if r == 0:
            #Jei r = 0 generuojama puse paskutinės eilutes su 1 reiksmemis.
            return self.generate_last_row(m, 1)
        elif r == 1 and m == 1:
            #Jei r = 1 ir m = 1, grazinama bazine matrica.
            return [[1, 1], [0, 1]]
        else:
            #Rekursyviai sugeneruojamos matricos ir sudedamos i pilną matrica.
            lower_left = self.generate_last_row(m, 0)  
            lower_right = self.generate_matrix(r - 1, m) 

            bottom_matrix = self.combine_two_matrix_horizontally(lower_left, lower_right) 

            upper_left_and_upper_right = self.generate_matrix(1, m - 1) 

            top_matrix = self.combine_two_matrix_horizontally(upper_left_and_upper_right, upper_left_and_upper_right) 

            result = self.combine_two_matrix_vertically(top_matrix, bottom_matrix)  
            return result

    def encode(self, message, m):
        # Užkoduoja pranešimą pagal RM(1, m) kodą.
        # Parametrai:
        # message - vektorius, kuris bus užkoduotas.
        # m - kodo ilgio parametras.
        # Grąžina užkoduotą pranešimą.

        matrix = self.generate_matrix(1, m) 
        return self.multiply_matrix_and_vector(matrix, message) 
