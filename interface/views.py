import json
import os
import shutil
import subprocess

import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from social.apps.django_app.default.models import UserSocialAuth

from interface.models import Build, Repo
from interface.utils import get_github


class BuildDetailView(DetailView):
    model = Build


class RegisterRepoView(ListView, LoginRequiredMixin):
    template_name = 'interface/register_repo.html'

    def get_queryset(self):
        # Get list of user repos
        g = get_github(self.request.user)
        return g.get_user().get_repos()


@login_required
def ProcessRepo(request, full_name):
    user = request.user
    g = get_github(user)

    grepo = g.get_repo(full_name)

    hook = grepo.create_hook(
        'web',
        {
            'content_type': 'json',
            'url': request.build_absolute_uri(reverse('webhook'))
        },
        events=['push'],
        active=True
    )

    repo = Repo.objects.create(full_name=grepo.full_name, user=user, webhook_id=hook.id)

    url = reverse('repo_detail', kwargs={'pk': repo.id})
    return redirect(url)


@csrf_exempt
def WebhookView(request):
    try:
        body = json.loads(request.body)
    except ValueError:
        return HttpResponse('Invalid JSON body.', status=400)

    try:
        repo = Repo.objects.get(full_name=body['repository']['full_name'])
    except Repo.DoesNotExist:
        return HttpResponse(status=204)

    try:
        data = UserSocialAuth.objects.filter(user=repo.user).values_list('extra_data')[0][0]
    except:
        raise Exception('Fail')

    username = data['login']
    password = data['access_token']
    auth = (username, password)

    # get necessary vars
    repo_name = body['repository']['name']
    clone_url = body['repository']['clone_url']
    clone_url = clone_url.replace('github.com', '%s:%s@github.com' % (username, password))
    branch = body['ref'].replace('refs/heads/', '')
    combo_name = '/'.join([repo_name, branch])
    sha = body['head_commit']['id']
    status_url = body['repository']['statuses_url'].replace('{sha}', sha)

    build = Build.objects.create(
        repo=repo,
        ref=branch,
        sha=sha,
        status=Build.PENDING
    )

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
        status = 'success'
        publish_status(status, 'Your code conforms to pep8.')
    else:
        status = 'error'
        output = output.replace(directory, '')

    # save record
    build.status = status
    build.result = output
    build.finished_at = timezone.now()
    build.save()

    path = reverse('build_detail', kwargs={'pk': build.id})
    url = request.build_absolute_uri(path)
    publish_status('error', 'Your code has pep8 violations.', target_url=url)

    return HttpResponse(status=204)
