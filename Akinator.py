import pymysql
import sys

class Akinator:
    main_categories = ['소설', '만화', '참고서']
    sub_categories = [['로맨스', '스릴러', 'SF'],  # 소설에 대한 소분류
                      ['교육', '역사', '과학'],  # 만화에 대한 소분류
                      ['과학', '사회', '인문학']]  # 참고서에 대한 소분류

    Akinator_db = pymysql.connect(
        user='root',
        passwd='dnzl4001',
        host='127.0.0.1',
        db='bookakinator',
        charset='utf8'
    )

    def __init__(self):
        self.main_cat = int
        self.sub_cat = int
        self.selected_tags = []
        self.QM = QuestionManager()
        self.RM = ResultManager()
        print("<<<Book Akinator를 시작합니다.>>>")


    def read_book_DB(self):
        sql = "SELECT * FROM `Books`;"
        cursor = self.Akinator_db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        book_list = cursor.fetchall()
        return book_list


    def read_question_DB(self):
        sql = "SELECT * FROM `Questions`;"
        cursor = self.Akinator_db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        question_data = cursor.fetchall()
        return question_data

    def get_categories(self):
        self.main_cat = self.category_gui(self.main_categories) # 처음에 main category, sub category 입력받아서 저장
        self.sub_cat = self.category_gui(self.sub_categories[int(self.main_cat)], False)  # 처음에 main category, sub category 입력받아서 저장


    def call_QM(self):
        question_list_for_selected_category = self.make_trees()
        if len(question_list_for_selected_category) < 1:
            print("!ERROR! 질문 데이터가 존재하지 않습니다.")
            sys.exit()
        else:
            self.selected_tags = self.QM.get_tag_selection(question_list_for_selected_category)



    def call_RM(self):
        recommanded_book = self.choose_recommended_books(self.selected_tags)
        feedback = self.RM.show_result_and_get_feedback(recommanded_book)
        if feedback:
            print('사용자의 feedback:', feedback)
        else:
            print('피드백이 없습니다.')


    def make_trees(self,):
        question_data = self.read_question_DB()
        this_question = []
        for question in question_data:
            if question['main_category'] == int(self.main_cat) and question['sub_category'] == int(self.sub_cat):
                this_question.append([question['question'], question['tags']])
        return this_question


    def choose_recommended_books(self, selected_tag_list):
        total_book_list = self.read_book_DB()
        total_tag_list = []
        for book in total_book_list:
            total_tag_list.append(book['tags'])
        for bookTagsNum in range(len(total_tag_list)):
            isRightBook = True
            for sel_tag in selected_tag_list:
                if sel_tag in total_tag_list[bookTagsNum]:
                    pass
                else:
                    isRightBook = False
                    break
            if isRightBook:
                book = total_book_list[bookTagsNum]
                return book

    def category_gui(self, cat_list, isMain = True):
        if isMain:
            print("대분류 목록:")
        else:
            print("소분류 목록:")
        for i in range(len(cat_list)):
            print(i,'.',cat_list[i])
        while True:
            if isMain:
                selected_cat = input("대분류를 선택하세요: ")
            else:
                selected_cat = input("소분류를 선택하세요: ")
            if int(selected_cat) >= len(cat_list):
                print("!ERROR! 잘못된 입력입니다.")
            else:
                print('--------------------------------')
                return selected_cat

class QuestionManager:
    def __init__(self,):
        pass

    def get_tag_selection(self, question_list): # GUI와 상호작용하면서 tag selection 받는 함수
        modified_question = self.modify_questions(question_list)
        selected_tag_list = []
        question_cnt = 0
        while question_cnt < len(modified_question):
            # GUI를 통해 사용자와 상호작용하면서 tag selection 받음
            selected_tag = self.QM_gui(modified_question[question_cnt])
            if not selected_tag:
                print('이전 질문 다시 보내기')
                question_cnt -= 1
            else:
                selected_tag_list.append(selected_tag)
                question_cnt += 1

        return selected_tag_list

    def modify_questions(self, question_list):
        question = []
        for q in question_list:
            one_question = []
            one_question.append(q[0])
            for tag in q[1:]:
                one_question.append(tag.replace('[', '').replace(']', '').replace('\n', ''))
            question.append(one_question)
        return question



    def QM_gui(self, question):
        while True:
            try:
                print('--------------------------------')
                tag_list = question[1].split(',')
                print(question[0])
                for i in range(len(tag_list)):
                    print(i,'.', tag_list[i])
                selected_int = input("태그를 선택하세요(이전 질문으로 돌아가고 싶으면 -1 입력):")
                if int(selected_int) == -1:
                    return False
                else:
                    return tag_list[int(selected_int)]
            except:
                print("!ERROR! 잘못된 입력입니다.")


class ResultManager:

    def __init__(self):
        pass

    def show_result_and_get_feedback(self, recommanded_book):
        feedback = self.RM_gui(recommanded_book) # GUI를 통해 북 보여주고, 리턴값으로 feedback 받음
        if feedback:
            return feedback
        else:
            return False

    def RM_gui(self, recommanded_book):
        print('--------------------------------')
        if recommanded_book:
            print("<추천 도서>")
            for key, value in recommanded_book.items():
                if key == 'id' or key == 'main_category' or key == 'sub_category':
                    pass
                else:
                    print(key,':', value)
            feedback = input("피드백 있으세요?:")
            return feedback
        else:
            print('!ERROR! 추천 도서가 존재하지 않습니다.')


if __name__ == '__main__':
    Aki = Akinator()

    # main, sub category 입력 받아서 akinator에 전달
    Aki.get_categories()

    # main, sub category 이용해서 질문 리스트 뽑았고, QM에 전달.
    # QM이 질문 리스트를 가지고 사용자와 상호작용하며 selected tags를 아키네이터에게 반환
    Aki.call_QM()

    # 선택된 태그를 위에서 받았으니 그걸 가지고 도서 정보를 뽑아서 RM에게 넘겨줌. R
    # RM은 해당 도서를 출력해주고 피드백을 받아서 아키네이터에게 반환
    Aki.call_RM()


