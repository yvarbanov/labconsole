import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect


from . import database
from .models import LabConsole 

import openstack
from openstack.compute import compute_service
import json

def _connect():
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


def index(request):
    conn = _connect()
    vms = conn.compute.servers()
    user = request.META.get("HTTP_X_FORWARDED_USER")
    if not user:
       user = ""
    search = {"description":"student=" + user}
    projects = {}
    for project in conn.identity.projects(**search):
       projects[project.name] = []
       for vm in conn.compute.servers(all_tenants=1,project_id=project.id):
           projects[project.name].append(vm)

    return render(request, 'index.html', {'projects': projects, 'user': user })
    #return render(request, 'welcome/index.html', {
    #    'hostname': hostname,
    #    'database': database.info(),
    #    'count': PageView.objects.count()
    #})

def get_vm(self, name):
    """Get a VM by name."""
    vms = self._client.compute.servers()


def console(request, server):
    conn = _connect()
    body = {'os-getVNCConsole': {'type': 'novnc'}}
    headers = {'Accept': ''}
    resp = conn.session.post( '/servers/{server_id}/action'.format(server_id=server),json=body, headers=headers, endpoint_filter={'service_type': 'compute'})
    content = json.loads(resp.content)
    response = redirect(content["console"]["url"]) 
    return response


def health(request):
    return HttpResponse(1)

