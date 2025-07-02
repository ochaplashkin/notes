# usage: main.py [-h] [--truncate] [--drop] [--time TIME] [--time-delay TIME_DELAY] [--count COUNT]

# Simple data generator

# options:
#   -h, --help            show this help message and exit
#   --truncate            truncate table
#   --drop                drop table
#   --time TIME           time(seconds) to loading data
#   --time-delay TIME_DELAY
#                         delay(seconds) between load_data calls
#   --count COUNT         number of rows

import argparse
import json
import random
import uuid
import time
import os
from datetime import date

import psycopg2
import psycopg2.extras
from faker import Faker

fake = Faker()

psycopg2.extras.register_uuid()

DATABASE_URL = "postgresql://root@0.0.0.0:26000/postgres?sslmode=disable" or \
                os.environ['DATABASE_URL']


def generate_random_row():
    id_val = uuid.uuid4()
    a_val = random.randint(-9223372036854775808, 9223372036854775807)  # int8
    b_val = random.randint(-2147483648, 2147483647)  # int4
    c_val = random.randint(-32768, 32767)  # int2
    d_val = [random.randint(-32768, 32767) for _ in range(3)]  # _int2
    e_val = [random.randint(-2147483648, 2147483647) for _ in range(3)]  # _int4
    f_val = fake.text(max_nb_chars=32).strip().replace('\n', ' ')[:32]  # varchar(32)
    g_val = [fake.word() for _ in range(3)]  # _text
    h_val = fake.text(max_nb_chars=100)  # text
    i_val = json.dumps({"name": fake.name(), "age": random.randint(18, 90)})  # jsonb
    j_val = bytes(random.getrandbits(8) for _ in range(10))  # bytea
    k_val = round(random.uniform(-10000, 10000), 2)  # numeric
    l_val = random.choice([True, False])  # bool
    m_val = fake.text(max_nb_chars=50).strip().replace('\n', ' ')[:50]  # varchar
    n_val = fake.date_time(tzinfo=None)  # timestamptz
    o_val = fake.date_time()  # timestamp
    p_val = fake.date_between(start_date='-5y', end_date='today')  # date
    return (
        id_val, a_val, b_val, c_val, d_val, e_val, f_val, g_val,
        h_val, i_val, j_val, k_val, l_val, m_val, n_val, o_val, p_val
    )


def init(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS test (
                id UUID PRIMARY KEY,
                a int8,
                b int4,
                c int2,
                d _int2,
                e _int4,
                f varchar(32),
                g _text,
                h text,
                i jsonb,
                j bytea,
                k numeric,
                l bool,
                m varchar,
                n timestamptz,
                o timestamp,
                p date
            )
        """)
        print(f"init(): {cur.statusmessage}")
    conn.commit()


def load_data(conn, rows_count):
    with conn.cursor() as cur:
        for _ in range(rows_count):
            row = generate_random_row()
            cur.execute(
                """
                INSERT INTO test (
                    id, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                row
            )
            print(f"load_data(): {str(row[0]).split('-')[0]}")
    conn.commit()


def drop(conn):
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS test")
        print(f"drop(): {cur.statusmessage}")
    conn.commit()


def truncate(conn):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE test")
        print(f"truncate(): {cur.statusmessage}")
    conn.commit()


def main():
    parser = argparse.ArgumentParser(description="Simple data generator")
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="truncate table"
    )
    parser.add_argument(
        "--drop",
        action="store_true",
        help="drop table"
    )
    parser.add_argument(
        "--time",
        type=int,
        default=0,
        help="time(seconds) to loading data"
    )
    parser.add_argument(
        "--time-delay",
        type=float,
        default=0,
        help="delay(seconds) between load_data calls"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=0,
        help="number of rows"
    )
    args = parser.parse_args()

    with psycopg2.connect(DATABASE_URL) as conn:
        init(conn)
        if args.time > 0:
            print(f"load_data by time: {args.time} sec ...")
            start_time = time.time()
            while time.time() - start_time < args.time:
                load_data(conn, rows_count = 1)
                if args.time_delay > 0:
                    time.sleep(args.time_delay)

        if args.count > 0:
            print(f"load_data by count: {args.count} rows ...")
            load_data(conn, rows_count = args.count)

        if args.truncate:
            truncate(conn)
        if args.drop:
            drop(conn)
        print("done.")
        return


if __name__ == "__main__":
    main()
