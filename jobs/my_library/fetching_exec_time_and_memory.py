# coding: utf-8

"""
実行時に引数がproblem_idを表す引数が必要

該当するFileのレコードごとに、URLにアクセスして、memoryとtimeの値をスクレイピングする(それぞれ単位はKB, ms、多分)
スクレイピングしてきたら、verdict, memory timeとして、新テーブルに保存していく
"""

import os
import mysql.connector as cn
import sys
import requests 

class Connector:
    cnx = cn.connect(
    host='127.0.0.1',
    user='kosuke',
    password='localhost',
    port='3306',
    database='codeforces'
    )
    cur = cnx.cursor(buffered=True, dictionary=True)

    
    def execSelectSqlStatement(self, sql):
        Connector.cur.execute(sql)
        return Connector.cur.fetchall()

    def execInsertSqlStatement(self, sql):
        Connector.cur.execute(sql)
        Connector.cnx.commit()

"""
各problem_id毎にインスタンスを生成する
データ取得までにやること
1. problem_idが妥当か判断
2. submission_idの一覧を取得
3. 各submissionごとにAPIリクエストを送る
4. 新テーブルに取得したデータを格納する
"""
class Problem(Connector):
    # 引数がinvalid(Fileテーブルに解答が存在しなければ何もしない)
    def __init__(self, competition_id):
        self.competition_id = int(competition_id)
        sql = "SELECT count(*) as cnt FROM File WHERE competition_id = %d" %  self.competition_id
        sqlResult = super().execSelectSqlStatement(sql)
        if int(sqlResult[0]['cnt']) != 0:
            self.execAllProcess()

    def execAllProcess(self):
        self.submissionList = self.getSubmissionList()
        self.resultsAPI = self.submitAPIRequest()
        for submission in self.submissionList:
            id = submission['submission_id']
            record = self.getValue(id, self.resultsAPI['result'])

            # 既存レコードのsubmission_id1件ごとに対して、そんざ
            sql = "SELECT count(*) as cnt FROM SubmissionStatus WHERE submission_id = %d" % id
            count = super().execSelectSqlStatement(sql)
            print(count[0]['cnt'])
            if(count[0]['cnt'] == 0):
                print(record)
                sql = "INSERT INTO SubmissionStatus (submission_id, verdict, timeConsumedMillis, memoryConsumedBytes) VALUES (%d, '%s' , %d, %d);" % (id, record['verdict'], record['timeConsumedMillis'], record['memoryConsumedBytes'])
                super().execInsertSqlStatement(sql)
                print('finish to insert record of %s' % id )
            else: 
                print('already exist record of %s' % id)

    def getValue(self, id, items):
        values = [x for x in items if 'id' in x and  x['id'] == id]
        return values[0] if values else None


    def submitAPIRequest(self):
        base_url = 'http://codeforces.com/'
        url = base_url + 'api/'
        api = "contest.status?contestId=%d&from=1" % self.competition_id
        request = requests.get(url+api)
        return request.json()
    
    def getSubmissionList(self):
        sql = "select * from File WHERE competition_id = %d" % self.competition_id
        return super().execSelectSqlStatement(sql)

def main():
    args = sys.argv
    # 引数がなければそのまま終了
    if len(args) != 1:
        # 各引数の文字列ごとにProblemクラスを作成、データ取得とDB保存を実行
        for problem_id in args[1:]:
            problem = Problem(problem_id)


if __name__ == "__main__":
    main()