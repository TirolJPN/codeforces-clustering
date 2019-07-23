
import subprocess
import sys
from my_library import Connector

def main():
    connector = Connector.Connector()
    sql = "SELECT problem_id , count(*) as cnt FROM File WHERE problem_id IS NOT NUll AND verdict = \"OK\" AND (lang = \"GNU C++14\" OR lang = \"GNU C++11\" OR lang = \"GNU C++\") GROUP BY problem_id HAVING count(*) > 100 ORDER BY problem_id DESC"
    problems = connector.exec_select_sql(sql) 
    args = ' '.join([problem['problem_id'] for problem in problems])
    scripts = ['create_io_files_for_ngweight.py', 'create_vectors_of_ngram.py', 'lexical_clustering.py', 'metrical_clustering.py', 'visualize_clustering.py', 'count_cluster_elements.py']
    for script in scripts:
        print('---------------------------------------------%s-----------------------------------------' % script)
        cmd = "python %s %s" % (script, args)
        try:
            res = subprocess.run(cmd, shell=True)
        except:
            pass

if __name__ == '__main__':
    main()
