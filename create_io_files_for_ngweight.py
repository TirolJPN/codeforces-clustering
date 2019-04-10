import os
import mysql.connector as cn
from enum import  Enum
from dotenv import load_dotenv
import re
import subprocess
import sys
import key
from ./../my_library/Connector import Connector

"""
code from http://maku77.github.io/python/io/remove-java-comments.html
"""
class State(Enum):
    CODE = 1
    C_COMMENT = 2
    CPP_COMMENT = 3
    STRING_LITERAL = 4

"""
problem_idを引数として、ngweight用の1つの入力ファイルを作成する
"""
class FilesCreater(Connector):
    def __init__(self, problem_id):
        super().__init__()
        PATH_FEATURE_WORD_VECTORS = key.PATH_FEATURE_WORD_VECTORS
        PATH_SRC = key.PATH_SRC
        path_file = PATH_FEATURE_WORD_VECTORS + problem_id + '.txt'
        # 入力ファイルがまだ作成されていなければ実行する
        if not os.path.isfile(path_file):
            answers = self.get_right_answers(problem_id)
            with open(path_file, mode='w', encoding='utf-8') as f_ngweight:
                for answer in answers:
                    # 各解答のソースコードをngweight用のテキストファイルに追記していく
                    path_answer = PATH_SRC +  answer['file_name']
                    with open(path_answer, mode='r', encoding='utf-8') as f_src:
                            code_content = f_src.read()
                    # ヘッダーにファイル名を入れておく
                    f_ngweight.write(chr(2))
                    f_ngweight.write(answer['file_name'])
                    f_ngweight.write(chr(3))
                    s = self.filter_cpp_comment(code_content)
                    # 特殊記号をとりあえず空白に変換する
                    # processed_s = re.sub("\!|\?|\"|\'|#|\$|%|&|\||\(|\)|\{|\}|\[|\]|=|<|>|\+|-|\*|\/|\\|\~|\^|@|:|;|,|\.|\s+", " ", s)
                    processed_s = re.sub("\s+", " ", s)
                    #改行・スペースのスペース変換による連続スペースが残るので、それらも一つのスペースにする
                    processed_s = re.sub(r" +", " ", processed_s)
                    f_ngweight.write(processed_s)
            # pythonスクリプトからngweightを直接実行し、出力ファイルを得る
            cmd = "../../ngweight/bin/default/ngweight -w -s 0 < ../outputs/input_files/%s.txt > ../outputs/output_files/%s_output" % (problem_id, problem_id)
            res = subprocess.run([cmd], stdout=subprocess.PIPE, shell=True)
            sys.stdout.buffer.write(res.stdout)


    def filter_cpp_comment(self, text):
        """ Removes Java (C/C++) style comments from text. """
        result = []  # filtered text (char array)
        prev = ''  # previous char
        prevprev = ''  # previous previous char
        state = State.CODE
        for ch in text:
            # Skip to the end of C-style comment
            if state == State.C_COMMENT:
                if prevprev != '\\' and prev == '*' and ch == '/':  # End comment
                    state = State.CODE
                    prevprev = prev = ''
                elif ch == '\n':
                    result.append('\n')
                    prevprev = prev = ''
                else:
                    prevprev, prev = prev, ch
                continue
            # Skip to the end of the line (C++ style comment)
            if state == State.CPP_COMMENT:
                if ch == '\n':  # End comment
                    state = State.CODE
                    result.append('\n')
                    prevprev = prev = ''
                continue
            # Skip to the end of the string literal
            if state == State.STRING_LITERAL:
                if prev != '\\' and ch == '"':  # End literal
                    state = State.CODE
                result.append(prev)
                prevprev, prev = prev, ch
                continue
            # Starts C-style comment?
            if prevprev != '\\' and prev == '/' and ch == '*':
                state = State.C_COMMENT
                prevprev = prev = ''
                continue
            # Starts C++ style comment?
            if prevprev != '\\' and prev == '/' and ch == '/':
                state = State.CPP_COMMENT
                prevprev = prev = ''
                continue
            # Comment has not started yet
            if prev: result.append(prev)
            # Starts string literal?
            if ch == '"':
                state = State.STRING_LITERAL
            prevprev, prev = prev, ch
        # Returns filtered text
        if prev: result.append(prev)
        return ''.join(result)


    def get_right_answers(self, problem_id):
        lang_list = ['GNU C++14', 'GNU C++11', 'GNU C++']
        lang_select = '(%s)' % ' or '.join(["lang='%s'" % lang for lang in lang_list])
        sql = "SELECT * FROM File WHERE problem_id LIKE \"%s\" AND verdict = \"OK\" AND %s" % (problem_id, lang_select)
        return super().exec_select_sql(sql)


def main():
    args = sys.argv
    if len(args) != 1:
        for problem_id in args[1:]:     
            FilesCreater(problem_id)


if __name__ == '__main__':
    main()