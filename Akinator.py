
def get_book_list():
    book_list = []
    f = open("data/BookDB.txt", 'r', encoding='UTF-8')
    line = f.readline()
    while True:
        line = f.readline()
        if not line:
            break
        aBook = line.split(',')
        book_list.append(aBook)

    return book_list

def select_main_category(p_categories):
    selected = 1    # 사용자가 선택한 대분류 int
    return selected

def select_sub_category(p_categories):
    selected = 1  # 사용자가 선택한 소분류 int
    return selected

def get_next_question_list():
    pass

def get_previous_question_list():
    pass

def make_trees():
    pass

def send_recommended_books():
    pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_categories = ['소설', '만화', '참고서']
    sub_categories = [['로맨스', '스릴러', 'SF'], # 소설에 대한 소분류
                      ['교육', '역사', '과학'],   # 만화에 대한 소분류
                      ['과학', '사회', '인문학']]  # 참고서에 대한 소분류

    total_book_list = get_book_list()
    for book in total_book_list:
        print(book)


    #main_category = select_main_category(main_categories)
    #sub_category = select_sub_category(sub_categories)

