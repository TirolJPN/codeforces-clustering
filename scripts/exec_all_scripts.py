
import subprocess
import sys
from Connector import Connector


"""
TODO:
現時点で対応しているのは，「プリプロセッサそのまま，単記号含む」の場合だけ．
引数取って，残り3つの場合と，lexicalで実行時間とかを使った「先行研究の再現」が必要
"""
def main():
    connector = Connector()
    # Fileテーブルで，使用言語がC++かつverdictがOKな解答が1つ以上なproblem_idのリストを持ってくる
    # sql = "SELECT problem_id , count(*) as cnt FROM File WHERE problem_id IS NOT NUll AND verdict = \"OK\" AND (lang = \"GNU C++14\" OR lang = \"GNU C++11\" OR lang = \"GNU C++\") AND competition_id LIKE '6__' GROUP BY problem_id HAVING count(*) > 8 ORDER BY cnt DESC limit 50"
    sql = "SELECT problem_id , count(*) as cnt FROM File WHERE problem_id IS NOT NUll AND verdict = \"OK\" AND (lang = \"GNU C++14\" OR lang = \"GNU C++11\" OR lang = \"GNU C++\") AND (problem_id = '691A' OR problem_id = '691D' ) GROUP BY problem_id HAVING count(*) > 8 ORDER BY cnt DESC limit 50"
    problems = connector.exec_select_sql(sql) 
    args = ' '.join([problem['problem_id'] for problem in problems])
    # scripts = ['create_io_files_for_ngweight.py', 'create_vectors_of_ngram.py', 'exec_lexical_clustering.py', 'index_src.py', 'exec_metrical_clustering.py']
    # scripts = ['index_src.py', 'exec_metrical_clustering.py']
    scripts = ['create_scatter_plot.py']
    for script in scripts:
        print('---------------------------------------------%s-----------------------------------------' % script)
        cmd = "python %s %s" % (script, args)
        res = subprocess.run(cmd, shell=True)

if __name__ == '__main__':
    main()


# SELECT problem_id , count(*) as cnt FROM File WHERE problem_id IS NOT NUll AND verdict = "OK" AND (lang = "GNU C++14" OR lang = "GNU C++11" OR lang = "GNU C++") GROUP BY problem_id HAVING count(*) > 8  ORDER BY cnt DESC
