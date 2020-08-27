from datetime import datetime

import peewee

from settings import DATABASE

db = peewee.PostgresqlDatabase(**DATABASE)


class NifdcPrd(peewee.Model):
    goods_id = peewee.TextField(null=True)
    key_id = peewee.TextField(null=True)
    max_purchase = peewee.TextField(null=True)
    cat_no = peewee.TextField()
    cn_name = peewee.TextField(null=True)
    en_name = peewee.TextField(null=True)
    lot = peewee.TextField(null=True)
    package = peewee.TextField(null=True)
    price = peewee.FloatField(null=True)
    tax = peewee.FloatField(null=True)
    usage = peewee.TextField(null=True)
    catalog = peewee.TextField(null=True)
    storage = peewee.TextField(null=True)
    coa_url = peewee.TextField(null=True)

    created_at = peewee.DateTimeField(default=datetime.now)
    modified_at = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = db
        indexes = (
            (('cat_no', 'lot'), True),
        )


if __name__ == '__main__':
    NifdcPrd.create_table(safe=True)
