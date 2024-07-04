from database.DB_connect import DBConnect
from model.artObject import ArtObject
from model.connessione import Connessione


class DAO():
    @staticmethod
    def getAllObjects():
        cnx=DBConnect().get_connection()

        result=[]

        cursor=cnx.cursor(dictionary=True)
        query="""select * from objects o"""

        cursor.execute(query,())
        for row in cursor:
            result.append(ArtObject(**row))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getPeso(v1:ArtObject,v2:ArtObject):

        cnx = DBConnect().get_connection()

        result = []

        cursor = cnx.cursor(dictionary=True)
        query = """select count(*)
           from exhibition_objects eo1, exhibition_objects eo2
           where eo1.exhibition_id=eo2.exhibition_id and eo1.object_id<eo2.object_id
           and eo1.object_id=%s and eo2.object_id=%s"""

        cursor.execute(query, (v1.object_id,v2.object_id))
        for row in cursor:
            result.append(ArtObject(**row))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    #strada più difficile ma veloce
    def getAllConnessioni(idMap):
        cnx = DBConnect().get_connection()

        result = []

        cursor = cnx.cursor(dictionary=True)
        query = """select eo1.object_id as o1,eo.object_id as o2, count(*) as peso
        from exhibition_objects eo1, exhibition_objects eo2
        where eo1.exhibition_id=eo2.exhibition_id and eo1.object_id<eo2.object_id
        group by eo1.object_id,eo2.object_id
        order by peso desc"""

        cursor.execute(query, ())
        for row in cursor:
            result.append(Connessione(idMap[row["o1"]],idMap[row["o1"]],row["peso"]))

        cursor.close()
        cnx.close()
        return result