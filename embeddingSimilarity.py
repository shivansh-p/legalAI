import psycopg2
import openai
import os
import utilityFunctions as util
from utilityFunctions import get_embedding
from utilityFunctions import psql_connect


def main():
    pass
    
# Internal tool for testing embedding similarity
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
        compare_content_embeddings(user_text, user_match_threshold, user_match_count)
        print()

# Return most relevant content embeddings
def compare_content_embeddings(text, print_relevant_sections=False, match_threshold=0.5, match_count=5):
    embedding = get_embedding(text)
    conn = psql_connect()
    cur = conn.cursor()

    cur.callproc('match_embedding', ['{}'.format(embedding), match_threshold, match_count])
    #print("Fetching {} content sections with threshold {} for text:\n{}\n".format(match_count, match_threshold, text))
    result = cur.fetchall()
    cur.close()
    conn.close()
    #return result
    if print_relevant_sections:
        rows_formatted = format_sql_rows(result)
        print(rows_formatted)
    return result

# Return most relevant definition embeddings  
def compare_definition_embeddings(text, print_relevant_sections=False, match_threshold=0.5, match_count=5):
    embedding = get_embedding(text)
    conn = psql_connect()
    cur = conn.cursor()
    cur.callproc('match_definitions', ['{}'.format(embedding), match_threshold, match_count])
    print("Fetching {} definition sections with threshold {} for text:\n{}\n".format(match_count, match_threshold, text))
    result = cur.fetchall()
    cur.close()
    conn.close()
    if print_relevant_sections:
        rows_formatted = format_sql_rows(result)
        #print(rows_formatted)
    return result

# Return most relevant header embeddings
def compare_header_embeddings(text, print_relevant_headers=False, match_threshold=0.5, match_count=5):
    embedding = get_embedding(text)
    conn = psql_connect()
    curr = conn.cursor()
    # cur.callproc
    result = curr.fetchall()
    curr.close()
    conn.close()
    if print_relevant_headers:
        rows_formatted = format_sql_rows(result)
    return result

# Format one row of the table in a string, adding universal citation (State Code § Section #)
def format_sql_rows(list_of_rows):
    result =""
    for row in list_of_rows:
        result += "\n"
        
        result += "Cal. {} § {}:\n{}\n".format(row[2], row[8], row[9])
    result += "\n"
    return result

# Create Title and Definition Embeddings, previously createTitleDefinitionEmbedding.py
def createTitleDefinitionEmbedding():
    conn = psql_connect()
    sql_select = "SELECT id, definitions, title_path, content_tokens FROM ca_code ORDER BY id;"
    rows = util.select_and_fetch_rows(conn, sql_select)
    print(len(rows))
    conn.close()
    conn = psql_connect()
    get_all_row_embeddings(rows, conn)

# Get embeddings from openAI for new title/definitions
def get_all_row_embeddings(rows, conn):
    titleDict = {}
    defDict = {}
    cursor = conn.cursor()
    for tup in rows:
        id = int(tup[0])
        
        definitions = tup[1]
        title_path = tup[2]
        content_tokens = tup[3]
        sql_update = "UPDATE ca_code SET "
        if definitions in defDict:
            print("Definition already in defDict for id: {}".format(id))
            def_embedding = defDict[definitions][0]
            def_tokens = defDict[definitions][1]
        else:
            try:
                def_embedding, def_tokens = util.get_embedding_and_token(definitions)
                print("New definition found for id: {}".format(id))
                defDict[definitions] = [def_embedding, def_tokens]
                sql_update += "definition_embedding='{}', ".format(def_embedding)
            except:
                def_tokens = 0
        if title_path in titleDict:
            title_embedding = titleDict[title_path][0]
            title_tokens = titleDict[title_path][1]
        else:
            try:
                title_embedding, title_tokens = util.get_embedding_and_token(title_path)
                titleDict[title_path] = [title_embedding, title_tokens]
                sql_update += "title_path_embedding='{}', ".format(title_embedding)
            except:
                title_tokens = 0
            
        total_tokens = content_tokens+def_tokens+title_tokens
        sql_update +=  " titles_tokens='{}', definition_tokens='{}', total_tokens='{}' WHERE id='{}';".format(title_tokens, def_tokens, total_tokens, id)
        cursor.execute(sql_update)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()