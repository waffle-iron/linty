import json
import os

import subprocess

import shutil

import requests
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from interface.models import Result


class ResultDetailView(DetailView):
    model = Result


@csrf_exempt
def WebhookView(request):
    try:
        body = json.loads(request.body)
    except ValueError:
        return HttpResponse('Invalid JSON body.', status=400)

    # TODO: get credentials from User
    username = os.environ.get('GITHUB_USERNAME')
    password = os.environ.get('GITHUB_TOKEN')
    auth = (username, password)

    # get necessary vars
    repo_name = body['repository']['name']
    clone_url = body['repository']['clone_url']
    clone_url = clone_url.replace('github.com', '%s:%s@github.com' % (username, password))
    branch = body['ref'].replace('refs/heads/', '')
    combo_name = '/'.join([repo_name, branch])
    sha = body['head_commit']['id']
    status_url = body['repository']['statuses_url'].replace('{sha}', sha)

    def publish_status(state, description, target_url=None):
        data = {
            'state': state,
            'description': description,
            'target_url': target_url,
            'context': 'linty'
        }
        requests.post(status_url, json=data, auth=auth)

    publish_status('pending', 'Linting your code...')

    # download repo
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    directory = 'tmp/%s' % combo_name
    if os.path.exists(directory):
        shutil.rmtree(directory)
    subprocess.call(['git', 'clone', clone_url, directory])
    subprocess.call(['git', '--git-dir=%s/.git' % directory, '--work-tree=%s' % directory, 'fetch', clone_url])
    subprocess.call(['git', '--git-dir=%s/.git' % directory, '--work-tree=%s' % directory, 'checkout', branch])

    # run pep8
    output = None
    try:
        subprocess.check_output(['pep8', directory])
    except subprocess.CalledProcessError as e:
        # pep8 returns a non-zero code when it finds issues, so we have to catch the error to get the output
        output = e.output

    if not output:
        publish_status('success', 'Your code conforms to pep8.')
    else:
        output = output.replace(directory, '')
        # save record
        result = Result.objects.create(text=output)
        path = reverse('result_detail', kwargs={'pk': result.id})
        url = request.build_absolute_uri(path)
        publish_status('error', 'Your code has pep8 violations.', target_url=url)

    return HttpResponse(status=204)
