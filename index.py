from app_config import configure

from integrations.controller import integration_controller
from src import init_app
from apscheduler.schedulers.background import BackgroundScheduler

configuration = configure['development']
app = init_app(configuration)

# Agregar esta línea para definir la variable 'application'
application = app

task = BackgroundScheduler()
task.add_job(integration_controller, 'interval', seconds=10) 
task.start()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)