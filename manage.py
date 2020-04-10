from flask_script import Manager
from celery import Celery

from odk import create_app


# 创建app
app = create_app('dev')

# 添加celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# 添加管理
manager = Manager(app)

# 数据库迁移管理
# Migrate(app, db)
# manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()




