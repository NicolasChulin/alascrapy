import pymysql
from alascrapy.settings import DEFAULT_DB

class Pydb(object):

    def __init__(self,db_name=None):
        self.connect(db_name)

    def get_config(self,db_name=None):
        return {
            'host': DEFAULT_DB['HOST'],
            'port': DEFAULT_DB['PORT'],
            'user': DEFAULT_DB['USER'],
            'passwd': DEFAULT_DB['PASSWORD'],
            'db':db_name if db_name else DEFAULT_DB['NAME'],
            'charset':'utf8mb4',
            'cursorclass':pymysql.cursors.DictCursor
        }

    def get_wheres(self,whered):
        wheres = []
        for k,v in whered.items():
            wheres.append("%s='%s'" % (k,v))
        return ' and '.join(wheres)

    def get_sets(self,setd):
        sets = []
        for k,v in setd.items():
            sets.append("%s='%s'" % (k,v))
        return ','.join(sets)

    def connect(self,db_name=None):
        config = self.get_config(db_name)
        self.conn = pymysql.connect(**config)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def commit(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()

    def filter(self,tb_name,whered):
        wheres = self.get_wheres(whered)
        sql="SELECT * FROM %s WHERE %s" % (tb_name,wheres)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def create(self,tb_name,data):
        keys=[]
        values=[]
        for k,v in data.items():
            keys.append(k)
            values.append('"%s"' % v)
        sql="INSERT INTO %s (%s) VALUES (%s)" % (tb_name,','.join(keys),','.join(values))
        self.commit(sql)

    def update(self,tb_name,setd,whered):
        sets = self.get_sets(setd)
        wheres = self.get_wheres(whered)
        sql="UPDATE %s SET %s WHERE %s" % (tb_name,sets,wheres)
        self.commit(sql)

    def delete(self,tb_name,whered):
        wheres = self.get_wheres(whered)
        sql="DELETE FROM %s WHERE %s" % (tb_name,wheres)
        self.commit(sql)

    def get_first_item(self,tb_name,whered):
        wheres = self.get_wheres(whered)
        sql="SELECT * FROM %s WHERE %s ORDER BY id desc LIMIT 1" % (tb_name,wheres)
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0]

    def get_count(self,tb_name,whered=None):
        if whered is None:
            sql="SELECT COUNT(1) AS num FROM %s" % (tb_name)
        else:
            wheres = self.get_wheres(whered)
            sql="SELECT COUNT(1) AS num FROM %s WHERE %s" % (tb_name,wheres)
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0]['num']








