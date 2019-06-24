from celery_example import make_celery
from app import app
from flask_sqlalchemy import SQLAlchemy
from models.runtime import RuntimeModel

from celery.utils.log import get_task_logger
import docker

client = docker.from_env()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379',
    CELERY_ALWAYS_EAGER = False
)

from db import db

db.init_app(app)

celery = make_celery(app)
logger = get_task_logger(__name__)

@celery.task(name='aon_container', bind=True)
def aon_container(self,data):

    print ("Current request id is ", self.request.id)
    runtime_id = data['runtime_id']

    print ("Searching for runtime id ", runtime_id)
    runtime = RuntimeModel.query.filter_by(id=runtime_id).first()

    create_dockerfile(self.request.id,runtime.dockerfile)
    create_container(self.request.id)

    container = run_container(self.request.id)

    #aon_clean_container(60, container, folder=self.request.id)


    print ("from database got runtime ", runtime.json())


    return {'runtime': runtime.json(), 'container_id': self.request.id }


def create_dockerfile(unique_dir, content):
    import os
    os.mkdir(unique_dir)
    f = open(unique_dir+"/Dockerfile", "w")
    f.write(content)
    f.close()

def create_container(folder):
    print ("Creating container of dockerfile in ", folder)
    try:
        output = client.images.build(path=folder, tag=folder)
        print ("Output from container creation ", output)
    except docker.errors.BuildError as e:
        print ("Raised ", e)


def run_container(container_name):

    root_path = app.root_path
    print ("Mouting from local ", root_path+"/"+container_name )

    container = client.containers.run(image=container_name, detach=True, auto_remove=True, volumes={root_path+"/"+container_name : {
        'bind': "/"+container_name, 'mode': 'rw', 'bind-propagation' : "shared"
    }}, publish_all_ports=True)


    print ("Logs: ", container.logs())
    return container

import time
#@celery.task(name='aon_clean_container', bind=True)

def aon_clean_container(duration, container, folder, remove_image=True):
    print ("Waiting for {} seconds to remove container {}".format(duration, container.name))
    time.sleep(duration)
    container.stop()
    print ("Container stopped.")
    image_id = container.image.attrs['Id'].split(':')[1]


    if(remove_image):
        print("Removing Image", image_id)
        try:
            client.images.remove(image_id)
        except Exception as e:
            print ("Could not remove image : ", e)
    else:
        print ("No image to remove")

    repos = container.image.attrs['RepoTags']
    if(remove_image):
        #clean all repos which has no corresponding running image
        for repo in repos:
            repo_tag = repo.split(':')[0]
            print("Removing repo", repo_tag)
            try:
                client.images.remove(repo_tag)
            except Exception as e:
                print ("Could not clean repo ", e)

            print ("\n\n")

    import shutil
    try:
        shutil.rmtree(folder)
    except Exception as e:
        print ("Could not remove folder: {} because {}".format(folder,str(e)))


