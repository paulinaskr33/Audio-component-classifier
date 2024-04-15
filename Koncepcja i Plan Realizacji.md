#### Inga Dyląg, Paulina Skrzypczak, Karolina Źróbek

Sztuczna Inteligencja w Systemach Informatycznych 2024

---
# Klasyfikator komponentów audio

### Temat projektu
Celem projektu jest stworzenie klasyfikatora komponentów audio, który będzie w stanie rozpoznawać różne dźwięki na nagraniach. Przykładowo, jeśli na nagraniu znajdują się dźwięki kluczy, klawiatury i deszczu, klasyfikator będzie w stanie rozpoznać te trzy dźwięki.

### Metody
1. **Uczenie nienadzorowane do rozdzielania komponentów audio**: Wykorzystamy algorytm Independent Component Analysis (FastICA) z pakietu scikit-learn. FastICA jest techniką która pozwala na rozdzielenie sygnału na jego składowe niezależne.
![Blind source separation using FastICA](https://scikit-learn.org/stable/_images/sphx_glr_plot_ica_blind_source_separation_001.png)
2. **Deep Learning do klasyfikacji**: Do klasyfikacji wykorzystamy głębokie sieci neuronowe. Przetestujemy dwie architektury:
   - **Convolutional 2D (Conv2D)**: Warstwy konwolucyjne są efektywne w analizie obrazów i mogą być również skuteczne w analizie spektrogramów dźwiękowych.
   - **Long Short-Term Memory (LSTM)**: LSTM jest rodzajem rekurencyjnej sieci neuronowej, która jest efektywna w analizie sekwencji danych, co może być przydatne w przypadku analizy sekwencji dźwięków.

### Biblioteka do przetwarzania audio
Do przetwarzania audio użyjemy biblioteki [Kapre](https://github.com/keunwoochoi/kapre). Zalety korzystania z Kapre to:
- Szybkość i łatwość użycia (moliwość zastosowania jako warstwa modelu Keras),
- Odporność na błędy,
- Rozbudwana dokumentacja i dostępne tutoriale.

W naszym projekcie wykorzystujemy Kapre, ponieważ umożliwia ono przetwarzanie danych audio bezpośrednio w modelu Keras. Dodatkowo, Kapre oferuje szeroki zakres funkcji przetwarzania, takich jak obliczanie spektrogramów, normalizacja danych i dodawanie szumu, co czyni go wygodnym narzędziem do eksperymentowania z różnymi technikami przetwarzania audio w modelach uczenia maszynowego.

### Zbiór danych
Do treningu i testowania modelu użyjemy zbioru danych [Environmental Sound Classification 50](https://www.kaggle.com/datasets/mmoreaux/environmental-sound-classification-50?resource=download&select=esc50.csv), który zawiera sklasyfikowane pliki WAV z dźwiękami codziennego życia, takimi jak pisanie na klawiaturze, dzwonienie telefonu, szczekanie psa, deszcz itd. Do testowania modelu dodatkowo planujemy utworzyć własne próbki danych. 

### Źródła
- Choi, K., Joo, D., & Kim, J. (2017). Kapre: On-gpu audio preprocessing layers for a quick implementation of deep neural network models with keras. https://doi.org/10.48550/ARXIV.1706.05781
- Github: [seth814/Audio-Classification](https://github.com/seth814/Audio-Classification)
- Youtube: [Scikit-learn 109:Unsupervised Learning 13: Project - Separate mixed audio.](https://www.youtube.com/watch?v=v-6tYAoRZsw)


