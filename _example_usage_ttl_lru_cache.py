@ttl_lru_cache(maxsize=200, ttl=3600)
def frequently_called_db_function(parameter_1, parameter_2):
    # long running query

    qry = """
        select column_value from table_name where param_1 = {} and param_2 = '{}'
    """.format(parameter_1, parameter_2)

    db_res = system.db.runPrepQuery(qry)

    return db_res.getValueAt(0,0)
