import time
import random
import pandas as pd
from encoder import Encoder
from channel import Channel
from decoder import Decoder
import matplotlib.pyplot as plt

def run_experiment():
    p = 0.25  
    m_values = range(2, 13) 
    results = [] 
    
    for m in m_values:
        total_decode_time = 0
        correct_decodings = 0
        iterations = 5  

        for _ in range(iterations):
            message_length = m + 1
            message = [random.randint(0, 1) for _ in range(message_length)]

            encoder = Encoder()
            encoded_message = encoder.encode(message, m)

            channel = Channel(p)
            received_message = channel.send(encoded_message)

            decoder = Decoder()
            start_time = time.time()
            decoded_message = decoder.decode(received_message, m)
            decode_time = time.time() - start_time

            if decoded_message == message:
                correct_decodings += 1

            total_decode_time += decode_time

        avg_decode_time = total_decode_time / iterations
        results.append({
            "m": m,
            "Avg Decode Time (s)": avg_decode_time,
            "Correct Decodings": correct_decodings
        })

    df_results = pd.DataFrame(results)
    print(df_results)

    plt.figure(figsize=(10, 5))
    plt.plot(df_results["m"], df_results["Vidutinis dekodavimo laikas (s)"], marker="o", label="Vidutinis dekodavimo laikas (s)")
    plt.xlabel("m (Kodo parametras)")
    plt.ylabel("Vidutinis dekodavimo laikas (s)")
    plt.title("Vidutinis dekodavimo laikas vs Kodo parametras m")
    plt.grid()
    plt.legend()
    plt.show()

    return df_results


if __name__ == "__main__":
    run_experiment()
