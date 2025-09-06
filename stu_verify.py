import mysql.connector

def verify_student_login(spr_no: int, ph_no: str) -> bool:
    try:
        mydb = mysql.connector.connect(
            host="cnlbvh.h.filess.io",
            user="clgfees_towertrace",
            password="4227ca4efc7d0fa1193fef328a8792f427b6774e",
            database="clgfees_towertrace",
            port=3307
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT ph_no FROM stu WHERE spr_no = %s", (spr_no,))
        result = mycursor.fetchone()

        mycursor.close()
        mydb.close()

        if result:
            stored_ph = str(result[0])  # Ensure string comparison
            return stored_ph == ph_no

        return False

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False
