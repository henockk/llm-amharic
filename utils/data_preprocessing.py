import psycopg2
import re
import os
from dotenv import load_dotenv

load_dotenv()

class AmharicDataCleaner:
    def __init__(self, data=None):
        self.data = data

    @staticmethod
    def normalize_char_level_missmatch(input_token):
        replacements = [
            (re.compile(r'[ሃኅኃሐሓኻ]'), 'ሀ'),
            (re.compile(r'[ሑኁዅ]'), 'ሁ'),
            (re.compile(r'[ኂሒኺ]'), 'ሂ'),
            (re.compile(r'[ሔዄ]'), 'ሄ'),
            (re.compile(r'[ሕኅ]'), 'ህ'),
            (re.compile(r'[ኆሖኾ]'), 'ሆ'),
            (re.compile(r'[ሠ]'), 'ሰ'),
            (re.compile(r'[ሡ]'), 'ሱ'),
            (re.compile(r'[ሢ]'), 'ሲ'),
            (re.compile(r'[ሣ]'), 'ሳ'),
            (re.compile(r'[ሤ]'), 'ሴ'),
            (re.compile(r'[ሥ]'), 'ስ'),
            (re.compile(r'[ሦ]'), 'ሶ'),
            (re.compile(r'[ዓኣዐ]'), 'አ'),
            (re.compile(r'[ዑ]'), 'ኡ'),
            (re.compile(r'[ዒ]'), 'ኢ'),
            (re.compile(r'[ዔ]'), 'ኤ'),
            (re.compile(r'[ዕ]'), 'እ'),
            (re.compile(r'[ዖ]'), 'ኦ'),
            (re.compile(r'[ጸ]'), 'ፀ'),
            (re.compile(r'[ጹ]'), 'ፁ'),
            (re.compile(r'[ጺ]'), 'ፂ'),
            (re.compile(r'[ጻ]'), 'ፃ'),
            (re.compile(r'[ጼ]'), 'ፄ'),
            (re.compile(r'[ጽ]'), 'ፅ'),
            (re.compile(r'[ጾ]'), 'ፆ'),
            (re.compile(r'[ቊ]'), 'ቁ'),
            (re.compile(r'[ኵ]'), 'ኩ'),
            (re.compile(r'(ሉ[ዋአ])'), 'ሏ'),
            (re.compile(r'(ሙ[ዋአ])'), 'ሟ'),
            (re.compile(r'(ቱ[ዋአ])'), 'ቷ'),
            (re.compile(r'(ሩ[ዋአ])'), 'ሯ'),
            (re.compile(r'(ሱ[ዋአ])'), 'ሷ'),
            (re.compile(r'(ሹ[ዋአ])'), 'ሿ'),
            (re.compile(r'(ቁ[ዋአ])'), 'ቋ'),
            (re.compile(r'(ቡ[ዋአ])'), 'ቧ'),
            (re.compile(r'(ቹ[ዋአ])'), 'ቿ'),
            (re.compile(r'(ሁ[ዋአ])'), 'ኋ'),
            (re.compile(r'(ኑ[ዋአ])'), 'ኗ'),
            (re.compile(r'(ኙ[ዋአ])'), 'ኟ'),
            (re.compile(r'(ኩ[ዋአ])'), 'ኳ'),
            (re.compile(r'(ዙ[ዋአ])'), 'ዟ'),
            (re.compile(r'(ጉ[ዋአ])'), 'ጓ'),
            (re.compile(r'(ደ[ዋአ])'), 'ዷ'),
            (re.compile(r'(ጡ[ዋአ])'), 'ጧ'),
            (re.compile(r'(ጩ[ዋአ])'), 'ጯ'),
            (re.compile(r'(ጹ[ዋአ])'), 'ጿ'),
            (re.compile(r'(ፉ[ዋአ])'), 'ፏ')
        ]
        for pattern, replacement in replacements:
            input_token = pattern.sub(replacement, input_token)
        return input_token

    @staticmethod
    def remove_punc_and_special_chars(text):
        if text is None:
            raise ValueError("Input text cannot be None")
        try:
            normalized_text = re.sub(r'[\!\@\#\$\%\^\«\_\°\é\»\&\*\(\)\…\[\]\{\}\;\“\”\›\’\‘\"\'\:\,\.\‹\/\<\>\?\\\\|\`\´\~\-\=\+\፡\።\፤\;\፦\፥\፧\፨\፠\፣]', '', text)
            return normalized_text
        except Exception as e:
            raise ValueError(
                "An error occurred while removing punctuation and special characters from the input text. Exception: {}".format(e)) from e
    
    @staticmethod
    def remove_ascii_and_numbers(text_input):
        if text_input is None:
            raise ValueError("Input text cannot be None")
        try:
            rm_num_and_ascii = re.sub(r'[A-Za-z0-9]', '', text_input)
            return re.sub(r'[\'\u1369-\u137C\']+', '', rm_num_and_ascii)
        except Exception as e:
            raise ValueError(
                "An error occurred while removing ASCII characters and numbers from the input text. Exception: {}".format(e)) from e

    @staticmethod
    def remove_newline_and_extra_space(text):
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

    @staticmethod
    def remove_emojis(text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # Emojis
                                   u"\U0001F300-\U0001F5FF"  # Symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # Transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # Flags (iOS)
                                   u"\U00002500-\U00002BEF"  # Chinese characters
                                   u"\U00002702-\U000027B0"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U00010000-\U0010ffff"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\ufe0f"  # Combining enclosing keycap
                                   u"\u3030"
                                   "]+", flags=re.UNICODE)
        clean_text = emoji_pattern.sub('', text)
        return clean_text

def clean_data_and_store():

    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    db_port = os.getenv('DB_PORT')

    conn_params = {
        'dbname': db_name,
        'user': db_user,
        'password': db_password,
        'host': db_host,
        'port': db_port
    }

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        # Create the cleaned_articles table
        create_cleaned_table_query = """
        CREATE TABLE IF NOT EXISTS cleaned_articles (
            id SERIAL PRIMARY KEY,
            article TEXT NOT NULL,
            category TEXT NOT NULL
        );
        """
        cur.execute(create_cleaned_table_query)
        conn.commit()

        # Fetch data from the articles table
        cur.execute("SELECT id, article, category FROM articles")
        rows = cur.fetchall()

        cleaner = AmharicDataCleaner()

        for row in rows:
            article_id, article, category = row
            cleaned_article = cleaner.normalize_char_level_missmatch(article)
            cleaned_article = cleaner.remove_punc_and_special_chars(cleaned_article)
            cleaned_article = cleaner.remove_ascii_and_numbers(cleaned_article)
            cleaned_article = cleaner.remove_newline_and_extra_space(cleaned_article)
            cleaned_article = cleaner.remove_emojis(cleaned_article)

            # Insert cleaned data into cleaned_articles table
            insert_cleaned_query = """
            INSERT INTO cleaned_articles (article, category) VALUES (%s, %s)
            """
            cur.execute(insert_cleaned_query, (cleaned_article, category))

        conn.commit()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    print("Data cleaned and stored successfully")

clean_data_and_store()
