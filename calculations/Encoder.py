import numpy as np

class Encoder:
    def __init__(self):
        pass

    def generate_matrix(self, r, m):
        """
        Generuoja generatoriaus matricą RM(r, m) naudojant rekursiją.
        """
        if r == 0:
            return self.generate_half_last_row(m, 1)
        elif r == 1 and m == 1:
            return np.array([[1, 1], [0, 1]])
        else:
            zeros_matrix = self.generate_half_last_row(m, 0)
            ones_matrix = self.generate_matrix(r - 1, m)
            bottom_matrix = self.combine_two_matrix_h(zeros_matrix, ones_matrix)
            half_top_matrix = self.generate_matrix(1, m - 1)
            full_top_matrix = self.combine_two_matrix_h(half_top_matrix, half_top_matrix)
            result = self.combine_two_matrix_v(full_top_matrix, bottom_matrix)
            return result

    def combine_two_matrix_h(self, matrix1, matrix2):
        """
        Kombinuoja dvi matricas horizontaliai (matrica1 kairėje, matrica2 dešinėje).
        """
        return np.hstack((matrix1, matrix2))

    def combine_two_matrix_v(self, matrix1, matrix2):
        """
        Kombinuoja dvi matricas vertikaliai (matrica1 viršuje, matrica2 apačioje).
        """
        return np.vstack((matrix1, matrix2))

    def generate_half_last_row(self, m, num):
        """
        Generuoja eilutę su visais 1 arba visais 0 (priklausomai nuo `num`).
        """
        length = 2 ** (m - 1)
        return np.full((1, length), num)

    def multiply_matrix_and_vector(self, matrix, vector):
        """
        Daugina generatoriaus matricą ir vektorių, grąžina užkoduotą vektorių.
        """
        c = np.dot(vector, matrix) % 2
        return c.astype(int)

    def encode(self, message, m):
        """
        Užkoduoja žinutę `message` su RM(1, m) kodu.
        """
        matrix = self.generate_matrix(1, m)
        return self.multiply_matrix_and_vector(matrix, message)
