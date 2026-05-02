from django.db import connections

# Verificar tablas en write_db
cursor = connections['write_db'].cursor()
cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename")
print("WRITE_DB tablas:", [r[0] for r in cursor.fetchall()])

# Verificar tablas en read_db
cursor2 = connections['read_db'].cursor()
cursor2.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename")
print("READ_DB  tablas:", [r[0] for r in cursor2.fetchall()])
