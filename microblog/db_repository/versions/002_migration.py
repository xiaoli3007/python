from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
_user_old_20161025 = Table('_user_old_20161025', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nickname', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
    Column('about_me', VARCHAR(length=140)),
    Column('last_seen', DATETIME),
)

followers = Table('followers', post_meta,
    Column('follower_id', Integer),
    Column('followed_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['_user_old_20161025'].drop()
    post_meta.tables['followers'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['_user_old_20161025'].create()
    post_meta.tables['followers'].drop()
