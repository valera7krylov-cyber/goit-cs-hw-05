import string
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import matplotlib.pyplot as plt
import requests


def get_text(url):
    """Download text from the specified URL."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as error:
        print(f"Error downloading text: {error}")
        return None


def remove_punctuation(text):
    """Remove punctuation characters from the text."""
    return text.translate(
        str.maketrans("", "", string.punctuation)
    )


def map_reduce(text):
    """Count word frequencies using the MapReduce approach."""
    text = remove_punctuation(text)
    words = text.lower().split()

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduced_values = list(
            executor.map(reduce_function, shuffled_values)
        )

    return dict(reduced_values)


def map_function(word):
    """Map a word to a key-value pair."""
    return word, 1


def shuffle_function(mapped_values):
    """Group mapped values by word."""
    shuffled = defaultdict(list)

    for key, value in mapped_values:
        shuffled[key].append(value)

    return shuffled.items()


def reduce_function(key_values):
    """Reduce grouped values by summing their frequencies."""
    key, values = key_values
    return key, sum(values)


def visualize_top_words(word_counts, top_n=10):
    """Visualize the most frequent words."""
    top_words = sorted(
        word_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )[:top_n]

    words = [word for word, count in top_words]
    counts = [count for word, count in top_words]

    plt.barh(words[::-1], counts[::-1])
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title("Top Words by Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_words.png", dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    url = "https://www.gutenberg.org/cache/epub/1661/pg1661.txt"

    text = get_text(url)

    if text:
        result = map_reduce(text)

        top_words = sorted(
            result.items(),
            key=lambda item: item[1],
            reverse=True
        )[:10]

        print("Top 10 words:")

        for word, count in top_words:
            print(f"{word}: {count}")

        visualize_top_words(result)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")