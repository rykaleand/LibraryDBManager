from PyQt6.QtWidgets import QMessageBox

from DB_connection.dbconnect import connect_to_Database


def get_reader_menu_table(table,last_name, first_name):
    try:
        conn = connect_to_Database()
        cursor = conn.cursor()

        with open('SQl_files/reader_menu_select.sql', 'r') as file:
            query = file.read()

        update_query = query.format(table=table)

        conditions = []

        if (table != 'popular_books()'):
            if last_name:
                conditions.append(f" last_name = '{last_name}'")
            if first_name:
                conditions.append(f" first_name = '{first_name}'")

            # Добавляем условия к запросу
        if conditions:
            update_query += " WHERE"
            update_query += " AND ".join(conditions)

        cursor.execute(update_query)
        result = cursor.fetchall()
        conn.commit()

        return result
    except Exception as e:
        QMessageBox.warning(None, "Warning", f"Something went wrong: {str(e)}")
    finally:
        # Всегда закрываем курсор и соединение в блоке finally
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def delete_from_table(table,id):
    try:
        conn = connect_to_Database()
        cursor = conn.cursor()

        with open('SQl_files/delete_from_table.sql', 'r') as file:
            delete_query_template = file.read()

        delete_query = delete_query_template.format(table=table, id=id)
        cursor.execute(delete_query)
        conn.commit()
        QMessageBox.information(None, "Success", "Selected rows deleted successfully.")
    except Exception as e:
        QMessageBox.warning(None, "Warning", f"Something went wrong: {str(e)}")
    finally:
        # Всегда закрываем курсор и соединение в блоке finally
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def insert_table(table,headers, placeholders):
    try:
        conn = connect_to_Database()
        cursor = conn.cursor()

        with open('SQl_files/insert_table.sql', 'r') as file:
            insert_query_template = file.read()

        insert_query = insert_query_template.format(table=table, columns=headers, placeholders=placeholders)
        cursor.execute(insert_query)
        conn.commit()
        QMessageBox.information(None, "Success", "Changes saved successfully.")

    except Exception as e:
        QMessageBox.warning(None, "Warning", f"Something went wrong: {str(e)}")
    finally:
        # Всегда закрываем курсор и соединение в блоке finally
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def update_table(table, set_values, values):
    try:
        conn = connect_to_Database()
        cursor = conn.cursor()
        with open('SQl_files/update_table.sql', 'r') as file:
            sql_query_template = file.read()

        sql_query = sql_query_template.format(table=table, set_values=set_values, value=values[0])
        cursor.execute(sql_query)
        conn.commit()

    except Exception as e:
        QMessageBox.warning(None, "Warning", f"Something went wrong: {str(e)}")
    finally:
        # Всегда закрываем курсор и соединение в блоке finally
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def select_where_id(id, table):
    try:
        conn = connect_to_Database()
        cursor = conn.cursor()
        with open('SQl_files/select_where_id.sql', 'r') as file:
            sql_query_template = file.read()

        sql_query = sql_query_template.replace("{table}", table)
        cursor.execute(sql_query, (id,))
        result = cursor.fetchone()

        return result
    except Exception as e:
        QMessageBox.warning(None, "Warning", f"Something went wrong: {str(e)}")
    finally:
        # Всегда закрываем курсор и соединение в блоке finally
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def get_pass(login):
   try:
        conn = connect_to_Database()
        cursor = conn.cursor()
        with open('SQl_files/get_login.sql', 'r') as file:
            sql_query = file.read()

        cursor.execute(sql_query, (login,))

        result = cursor.fetchall()
        return result
   except Exception as e:
        QMessageBox.warning(None, "Warning", f"Something went wrong: {str(e)}")
   finally:
        # Всегда закрываем курсор и соединение в блоке finally
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_headers(table):
    try:
        conn = connect_to_Database()
        cursor = conn.cursor()
        with open('SQl_files/headers.sql', 'r') as file:
            sql_query_template = file.read()

        sql_query = sql_query_template.replace("{table}", table)
        cursor.execute(sql_query, (table,))
        result = [desc[0] for desc in cursor.description]

        return result

    except Exception as e:
        QMessageBox.warning(None, "Warning", f"Something went wrong: {str(e)}")
    finally:
        # Всегда закрываем курсор и соединение в блоке finally
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def print_table(table):
    try:
        conn = connect_to_Database()
        cursor = conn.cursor()
        with open('SQl_files/print_table.sql', 'r') as file:
            sql_query_template = file.read()

        sql_query = sql_query_template.replace("{table}", table)
        cursor.execute(sql_query, (table,))
        result = cursor.fetchall()

        return result
    except Exception as e:
        QMessageBox.warning(None, "Warning", f"Something went wrong: {str(e)}")
    finally:
        # Всегда закрываем курсор и соединение в блоке finally
        if cursor:
            cursor.close()
        if conn:
            conn.close()