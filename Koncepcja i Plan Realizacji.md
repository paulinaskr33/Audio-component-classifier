#### Inga Dyląg, Paulina Skrzypczak, Karolina Źróbek

Sztuczna Inteligencja w Systemach Informatycznych 2024

---
# Klasyfikator komponentów audio

### Temat projektu
Celem projektu jest stworzenie klasyfikatora komponentów audio, który będzie w stanie rozpoznawać różne dźwięki na nagraniach. Przykładowo, jeśli na nagraniu znajdują się dźwięki kluczy, klawiatury i deszczu, klasyfikator będzie w stanie rozpoznać te trzy dźwięki.

### Metody
1. **Uczenie nienadzorowane do rozdzielania komponentów audio**: Wykorzystamy algorytm Independent Component Analysis (FastICA) z pakietu scikit-learn. FastICA jest techniką która pozwala na rozdzielenie sygnału na jego składowe niezależne.

2. **Deep Learning do klasyfikacji**: Do klasyfikacji wykorzystamy głębokie sieci neuronowe. Przetestujemy dwie architektury:
   - **Convolutional 2D (Conv2D)**: Warstwy konwolucyjne są efektywne w analizie obrazów i mogą być również skuteczne w analizie spektrogramów dźwiękowych.
   - **Long Short-Term Memory (LSTM)**: LSTM jest rodzajem rekurencyjnej sieci neuronowej, która jest efektywna w analizie sekwencji danych, co może być przydatne w przypadku analizy sekwencji dźwięków.

### Biblioteka do przetwarzania audio
Do przetwarzania audio użyjemy biblioteki [Kapre]. Zalety korzystania z Kapre to:
- Możliwość optymalizacji parametrów przetwarzania sygnału,
- Szybkość i łatwość użycia,
- Odporność na błędy,
- Zgodność z różnymi formatami danych,
- Rozbudwana dokumentacja i dostępne tutoriale.

### Zbiór danych
Do treningu i testowania modelu użyjemy zbioru danych [Environmental Sound Classification 50](https://www.kaggle.com/datasets/mmoreaux/environmental-sound-classification-50?resource=download&select=esc50.csv), który zawiera sklasyfikowane pliki WAV z dźwiękami codziennego życia, takimi jak pisanie na klawiaturze, dzwonienie telefonu, szczekanie psa, deszcz itd. Do testowania modelu dodatkowo planujemy utworzyć własne próbki danych. 

### Źródła
- Choi, K., Joo, D., & Kim, J. (2017). Kapre: On-gpu audio preprocessing layers for a quick implementation of deep neural network models with keras. https://doi.org/10.48550/ARXIV.1706.05781
- Github: [seth814/Audio-Classification](https://github.com/seth814/Audio-Classification)
- Youtube: [Scikit-learn 109:Unsupervised Learning 13: Project - Separate mixed audio.](https://www.youtube.com/watch?v=v-6tYAoRZsw)

