from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


from odk import create_app, db


# 创建app
app = create_app('dev')


manager = Manager(app)

# 数据库迁移管理
Migrate(app, db)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()




