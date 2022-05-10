from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django import template
from . import database
from .models import LabConsole 
import openstack
from openstack.compute import compute_service
import os
import json
import yaml


def _connect(cloud):
    if os.getenv('OS_CLIENT_CONFIG_FILE'):
        return openstack.connection.Connection(cloud=cloud)
    else:
        server = os.getenv('OS_AUTH_URL')
        project = os.getenv('OS_PROJECT_NAME')
        username = os.getenv('OS_USERNAME')
        password = os.getenv('OS_PASSWORD')
        return openstack.connection.Connection(
                    auth=dict(
                    auth_url=server,
                    project_name=project,
                    username=username,
                    password=password,
                    project_domain_name="Default",
                    user_domain_name="Default"),
                    identity_api_version=3,
                    region_name="regionOne",
                )

def _vm_to_project(conn, user, projects):
    for project in conn.identity.projects():
        for tag in project.tags:
            if user in tag:
                if project.name not in projects.keys():
                    projects[project.name] = []
                for vm in conn.compute.servers(all_tenants=1,project_id=project.id):
                    projects[project.name].append(vm)
    return projects

def index(request):
    user = request.META.get("HTTP_X_FORWARDED_USER") or os.getenv('TEST_USER')
    if not user:
       user = ""
    projects = {}
    if os.getenv('OS_CLIENT_CONFIG_FILE'):
        with open(os.getenv('OS_CLIENT_CONFIG_FILE')) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        clouds = [*data['clouds'].keys()]
        for cloud in clouds:
            conn = _connect(cloud)
            projects = _vm_to_project(conn, user, projects)
    else:
        conn = _connect(None)
        projects = _vm_to_project(conn, user, projects)
    return render(request, 'index.html', {'projects': projects, 'user': user })

def start_vm(request, server, cloud):
    conn = _connect(cloud)
    conn.compute.start_server(server)
    return HttpResponse(1)

def stop_vm(request, server, cloud):
    conn = _connect(cloud)
    conn.compute.stop_server(server)
    return HttpResponse(1)

def restart_vm(request, server, cloud):
    conn = _connect(cloud)
    conn.compute.reboot_server(server, reboot_type="HARD")
    response = JsonResponse({'success': 1})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def rebuild_vm(request, server, name, image, cloud):
    conn = _connect(cloud)
    attrs = {"image": image}
    conn.compute.rebuild_server(server, name, "1234", **attrs)
    return HttpResponse(1)

def rescue_vm(request, server, image, cloud):
    conn = _connect(cloud)
    image = conn.image.find_image(image)
    conn.compute.rescue_server(server, admin_pass="", image_ref=image.id)
    return HttpResponse(1)

def unrescue_vm(request, server, cloud):
    conn = _connect(cloud)
    conn.compute.unrescue_server(server)
    return HttpResponse(1)

def console(request, server, cloud):
    conn = _connect(cloud)
    body = {'os-getVNCConsole': {'type': 'novnc'}}
    headers = {'Accept': ''}
    resp = conn.session.post( '/servers/{server_id}/action'.format(server_id=server),json=body, headers=headers, endpoint_filter={'service_type': 'compute'})
    content = json.loads(resp.content)
    vm = conn.compute.get_server(server)
    response = render(request, 'console.html', {'console': content["console"]["url"].replace("auto", "novello"), 'vm': vm})
    response["Access-Control-Allow-Origin"] = "*"
    return response

def health(request):
    return HttpResponse(1)
