from collections import Counter
from nltk.corpus import stopwords
import nltk

# Download stopwords if not already downloaded
nltk.download('stopwords')

def word_frequency(file_path):
    # Get the set of English stopwords from nltk
    stop_words = set(stopwords.words('english'))
    
    try:
        # Open the file and read its content
        with open(file_path, 'r') as file:
            text = file.read()
        
        # Normalize text: convert to lowercase and split into words
        words = text.lower().split()
        
        # Remove punctuation from words
        words = [word.strip('.,!?()[]{}:;"\'') for word in words]
        
        # Filter out stopwords
        filtered_words = [word for word in words if word not in stop_words]
        
        # Count the frequency of each unique word
        word_count = Counter(filtered_words)
        
        # Sort by frequency (ascending) and then alphabetically for tie-breaking
        sorted_word_count = sorted(word_count.items(), key=lambda x: (x[1], x[0]))
        
        i=1
        # Print the words and their frequencies
        for word, count in sorted_word_count[::-1]:
            if i==41:
                break
            print(f"{word}: {int(round(count/5.8,0))}")
            i+=1
    
    except FileNotFoundError:
        print("File not found. Please check the file path and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'your_file.txt' with the path to your text file
word_frequency('salvo_induction2.txt')
