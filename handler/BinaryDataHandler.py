from handler.DataHandler import DataHandler
from calculations.Channel import Channel
from calculations.Encoder import Encoder
from calculations.Decoder import Decoder

class BinaryDataHandler(DataHandler):
    def handle_without_encoding(self, input_data, p):
        self.channel = Channel(p)
        sent_message = self.channel.send(input_data)
        return sent_message

    def handle_with_encoding(self, input_data, p, m):
        """
        Užkoduoja pranešimą, siunčia jį per kanalą ir grąžina rezultatus.
        """
        # Užkodavimas
        encoded_message = self.encoder.encode(input_data, m)
        print(f"Užkoduota žinutė: {encoded_message}")

        # Kanalo modeliavimas
        self.channel = Channel(p)
        sent_message = self.channel.send(encoded_message)
        print(f"Po siuntimo kanalu: {sent_message}")

        # Klaidų analizė
        error_positions = self.decoder.get_error_positions(sent_message, encoded_message)
        print(f"Klaidų skaičius: {len(error_positions)}")
        print(f"Klaidų pozicijos: {error_positions}")

        # Dekodavimas
        decoded_message = self.decoder.decode(sent_message, m)
        print(f"Dekoduota žinutė: {decoded_message}")

        return {
            "encoded_message": encoded_message,
            "sent_message": sent_message,
            "error_positions": error_positions,
            "decoded_message": decoded_message
        }
