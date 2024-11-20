from handler.BinaryDataHandler import BinaryDataHandler
from calculations.Converter import Converter

def main():
    print("Rydo-Miulerio kodo demonstracija (RM(1, m))")
    
    # Vartotojo įvestis
    m = int(input("Įveskite m reikšmę (pvz., 3): "))
    p = float(input("Įveskite klaidų tikimybę p (pvz., 0.1): "))
    expected_length = m + 1  # Įvesties žinutės ilgis yra m + 1
    binary_message = input(f"Įveskite dvejetainę žinutę, kurios ilgis yra {expected_length}: ")
    
    # Konvertavimas į sveikųjų skaičių masyvą
    input_data = Converter.string_to_int_array(binary_message)
    
    if len(input_data) != expected_length:
        print(f"Klaida: žinutės ilgis turi būti {expected_length}.")
        return
    
    # Naudojame BinaryDataHandler
    handler = BinaryDataHandler()
    results = handler.handle_with_encoding(input_data, p, m)

if __name__ == "__main__":
    main()
