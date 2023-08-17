import psycopg2
import openai
import os
from embedCodes import get_embedding
import getPSQLConn

def main():
    user_embedding_search()


def user_embedding_search():
    print("=== Welcome to the user embedding search function! ===")
    print("-This function allows the user to input some user generated text and receive the closest \"match\" found in the California Legal Code.")
    print("-User generated text is converted into vector embeddings using OpenAI's text-embedding-ada-002 model.")
    print("-This vector embedding is compared to a database of embedding for the entire legal code using cosine similarity search.")
    print("-Please try inputting more complex phrases and questions. The more verbiose language you use the better testing I get!.")
    print()
    user_text = ""
    while True:
        print("You will be prompted to enter some parameters. Enter\'q\' any time to exit the function:")
        
        user_text = input("  1. Some user text to search/compare to the database:\n")
        if user_text == "q":
            exit(0)
        while True:
            try:
                user_match_threshold = float(input("  2. A match threshold between [0 to 1.0]. Higher values means a stricter search. Defaults to 0.5.\n"))
                if user_match_threshold >= 1 or user_match_threshold <= 0:
                    print("Please put a valid float in the range [0,1] exclusive.")
                    continue
                break
            except:
                if user_text == "q":
                    exit(0)
                print("Please put a valid float from [0,1] exclusive.")
        while True:
            try:
                user_match_count = int(input("  3. The number of maximum match_counts you would like to see (1-20).\n"))
                if user_match_count > 20 or user_match_count <= 0:
                    print("Please put a valid int in the range (1, 20) inclusive.")
                    continue
                break
            except:
                if user_match_count == "q":
                    exit(0)
                print("Please put a valid int in the range (1, 20) inclusive.")
        print()
        compare_all_embeddings(user_text, user_match_threshold, user_match_count)
        print()

    
    


def compare_all_embeddings(text, match_threshold=0.5, match_count=5):
    embedding = get_embedding(text)
    conn = getPSQLConn.connect()
    cur = conn.cursor()

    print("\n\n")
    cur.callproc('match_embedding', ['{}'.format(embedding), match_threshold, match_count])
    print("Fetching {} matching sections which have cosine similarity match threshold {} for text:\n{}\n".format(match_count, match_threshold, text))
    result = cur.fetchall()

    rows_formatted = format_sql_rows(result)
    print(rows_formatted)
    
    cur.close()
    conn.close()

def format_sql_rows(list_of_rows):
    result = ""
    for row in list_of_rows:
        result += "################################################\n"
        result += "Similarity Score: {}\n".format(row[1])
        result += "Code {} | Division {} | Title {} | Part {} | Chapter {} | Article {} | Section {}\n{}\n".format(*row[2:10])
    result += "################################################\n"
    return result

if __name__ == "__main__":
    main()