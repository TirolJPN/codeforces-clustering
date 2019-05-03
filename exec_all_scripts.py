
import subprocess
import sys
from Connector import Connector

def main():
    connector = Connector()
    sql = "SELECT problem_id , count(*) as cnt FROM File WHERE problem_id IS NOT NUll AND verdict = \"OK\" AND (lang = \"GNU C++14\" OR lang = \"GNU C++11\" OR lang = \"GNU C++\") AND (problem_id = '691A' OR problem_id = '691D' ) GROUP BY problem_id HAVING count(*) > 8 ORDER BY cnt DESC limit 50"
    problems = connector.exec_select_sql(sql) 
    args = ' '.join([problem['problem_id'] for problem in problems])
    scripts = ['create_scatter_plot.py']
    for script in scripts:
        print('---------------------------------------------%s-----------------------------------------' % script)
        cmd = "python %s %s" % (script, args)
        res = subprocess.run(cmd, shell=True)

if __name__ == '__main__':
    main()
