from database.DB_connect import DBConnect
from model.product import Product
from model.connessione import Connessione


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getColori():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = "select distinct (Product_color) from go_products"
        cursor.execute(query)

        for row in cursor:
            result.append(row[0]) # sono tuple da un elemento
            #print(row)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllProducts():
        conn = DBConnect.get_connection()

        result = []
        # per prendere tutti i prodotti
        cursor = conn.cursor(dictionary=True)
        query = "select * from go_products"
        cursor.execute(query)

        for row in cursor:
            result.append(Product(**row))
            # print(row)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getProductsColor(color):
        conn = DBConnect.get_connection()

        result = []
        # per prendere i prodotti filtrati per colore
        cursor = conn.cursor(dictionary=True)
        query = """ select * from go_products where Product_color = %s
                """
        cursor.execute(query, (color,))

        for row in cursor:
            result.append(Product(**row))
            # print(row)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnessioni(anno, prodotto, idMap): # sbagliata
        conn = DBConnect.get_connection()

        result = []
        # per prendere le connessioni, cioè collegamento tra due prodotti e il numero di vendite
        cursor = conn.cursor(dictionary=True)
        query = """ 
                select gds1.Product_number as p1, gds2.Product_number as p2, count(distinct(gds1.Date)) as vendite
                from go_daily_sales gds1, go_daily_sales gds2
                where gds1.Date = gds2.Date and gds1.Product_number < gds2.Product_number and 
                year(gds1.Date) = %s and gds1.Retailer_code = gds2.Retailer_code and 
                (gds1.Product_number = %s or gds2.Product_number = %s)
                group by gds1.Product_number, gds2.Product_number
                """
        cursor.execute(query, (anno, prodotto, prodotto))

        for row in cursor:
            result.append(Connessione(idMap[row["p1"]], idMap[row["p2"]], row["vendite"]))
            # print(row)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllConnessioni(colore, anno, idMap):
        conn = DBConnect.get_connection()

        result = []
        # per prendere le connessioni, cioè collegamento tra due prodotti e il numero di vendite
        cursor = conn.cursor(dictionary=True)
        query = """ 
                select t1.Product_number as p1, t2.Product_number as p2, count(distinct(t1.Date)) as vendite
                from (select gds.Retailer_code , gds.Product_number , gds.Date 
                from go_daily_sales gds, go_products gp 
                where gds.Product_number = gp.Product_number and gp.Product_color = %s and year(gds.Date) = %s) as t1
                left join
                (select gds.Retailer_code , gds.Product_number , gds.Date 
                from go_daily_sales gds, go_products gp 
                where gds.Product_number = gp.Product_number and gp.Product_color = %s and year(gds.Date) = %s) as t2
                on t1.Retailer_code = t2.Retailer_code and t1.Date = t2.Date
                where t1.Product_number < t2.Product_number
                group by t1.Product_number, t2.Product_number
                order by vendite desc
                """
        cursor.execute(query, (colore, anno, colore, anno))

        for row in cursor:
            result.append(Connessione(idMap[row["p1"]], idMap[row["p2"]], row["vendite"]))
            # print(row)
        cursor.close()
        conn.close()
        return result


