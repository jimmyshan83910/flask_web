import psycopg2
from psycopg2.extras import RealDictCursor


# Use class for futrue side project DB
class WeatherDB():
    def __init__(self):
        self.conn = psycopg2.connect(
            database = "jimmy_web", user = "postgres", password = "j3598418",
            host = "j-side-project.crv0ozn3ercx.ap-northeast-1.rds.amazonaws.com",
            port = "5432")
        self.conn.set_session(autocommit=True)
    
    def get_db(self):
        return self.conn.cursor(cursor_factory = RealDictCursor)
    
    # def close_db_connect(self):
    #     # # According to blow syntax, close cursor fail. How do i close it ??? or it's necessary????
    #     # self.conn.cursor(cursor_factory = RealDictCursor).close()
    #     self.conn.close()