# Task A5: Design an AI Application for Citizen Complaints

## A5.1: Sentiment and Summary
* **Lexicon-Based Sentiment Scorer (with Negation Handling)**:
  * *Design*: Maintain predefined dictionaries of positive words (`+1` score, e.g., "clean", "good", "improved") and negative words (`-1` score, e.g., "smoke", "terrible", "choking"). Tokenize the complaint text into words, iterate sequentially, and track a negation window (e.g., words like "not", "no", "never"). If a sentiment word immediately follows a negation word, invert its polarity (`+1` becomes `-1`). Sum the final scores to classify the complaint as Positive (`> 0`), Negative (`< 0`), or Neutral (`0`).
* **Extractive Summariser**:
  * *Design*: Split the complaint text into individual sentences and tokenize into words while filtering out common stopwords (e.g., "the", "is", "and"). Compute the frequency of each remaining important word across the entire text. Score every sentence by summing the frequencies of the important words it contains (normalized by sentence length to prevent bias toward overly long sentences). Select the top $k$ highest-scoring sentences in their original chronological order as the final summary.

---

## A5.2: Basic Chatbot
* **Rule-Based Chatbot Design**:
  * *Mechanism*: Normalize user input to lowercase and match keywords using regular expressions or keyword lookup lists to identify intent (e.g., `"pm2.5"`, `"air quality"`), target location (e.g., `"Adyar"`), and timeframe (e.g., `"today"`). Map the extracted entities into a parameterized SQL query against the `readings` and `stations` tables:
    ```sql
    SELECT AVG(r.pm25) 
    FROM readings r
    JOIN stations s ON r.station_id = s.station_id
    WHERE s.station_name = 'Adyar' AND DATE(r.timestamp) = DATE('now');
    ```
  * Format the retrieved numerical value into a predefined response template (e.g., *"The average PM2.5 in Adyar today is 42.5 µg/m³."*).
* **Limitations**:
  * Fails on typos, synonyms, or unexpected phrasing not explicitly programmed into rules.
  * Cannot maintain multi-turn conversational context or handle follow-up questions (e.g., *"What about yesterday?"*).
  * Rigidly bound to exact entity names and struggles with complex, multi-condition queries.

---

## Alternative Concept and Complexity Analysis
### Trained ML / Pre-trained Language Model vs Word List

* **Solution Overview**:
  * Replace the rule-based lexicon with a supervised Naive Bayes classifier trained on labeled complaint data (using TF-IDF or bag-of-words features) or a fine-tuned pre-trained Transformer language model (e.g., DistilBERT) from a library like Hugging Face.
* **Time per Complaint**:
  * *Word List*: $O(w)$ where $w$ is the number of words in the complaint—near-instantaneous hash-map lookups taking fractions
