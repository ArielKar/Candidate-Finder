import json

from django.core.exceptions import ValidationError
from django.core.serializers import serialize
from django.db import IntegrityError
from django.forms import model_to_dict
from django.http import HttpResponseBadRequest, HttpResponse

from django.views.decorators.csrf import csrf_exempt

from api.job.models import Opinion, Job

from .models import Note, Candidate


def match_candidates_to_job(job, candidates):
    """
        As mentioned in the doc, this matching approach is very naive,
        the system is "live" and constantly changing - also a very extensive match decisions sequence will not be enough
        to properly make a match decision - Deep Learning models are needed.
    """
    match_list = []
    job_skill = job.skill
    job_title_words = job.title.lower().split(" ")
    for candidate in candidates:
        if job_skill in candidate.skills.all():
            match_list.append(candidate)
            continue
        candidate_title_words = candidate.title.lower().split(" ")
        concatenated = job_title_words + candidate_title_words
        if len(set(concatenated)) < len(concatenated):
            match_list.append(candidate)
            continue

    return match_list


def candidate_suggestions(request):
    if request.method != 'GET':
        return HttpResponseBadRequest(json.dumps({'message': 'bad request'}), content_type='application/json')
    job_id = request.GET['job']
    if not job_id:
        raise ValidationError('missing required parameter job')
    job_obj = Job.objects.get(id=job_id)
    exclude = [op.id for op in job_obj.opinions.all()]
    candidates = Candidate.objects.all().exclude(id__in=exclude)
    matched_candidate = match_candidates_to_job(job_obj, candidates)
    response = serialize('json', matched_candidate)
    return HttpResponse(response, content_type='application/json', status=200)


@csrf_exempt
def candidate_opinion(request):
    if request.method == 'GET':
        job_id = request.GET['job']
        liked = Opinion.objects.filter(job_id=job_id, liked=True) \
            .exclude(job__status='CLOSED').order_by('created_at')
        response = serialize('json', liked)
        return HttpResponse(response, content_type='application/json', status=200)

    elif request.method == 'PUT':
        try:
            req_body = json.loads(request.body)
            job_id = req_body['job']
            candidate_id = req_body['candidate']
            liked = req_body['liked']
            new_opinion = Opinion(job_id=job_id, candidate_id=candidate_id, liked=liked)
            new_opinion.save()
            response = json.dumps(model_to_dict(new_opinion))
            return HttpResponse(response, content_type='application/json', status=201)
        except IntegrityError:
            return HttpResponseBadRequest(json.dumps({'message': 'bad request'}), content_type='application/json')
    return HttpResponseBadRequest(json.dumps({'message': 'bad request'}), content_type='application/json')


@csrf_exempt
def candidate_note(request, candidate_id):
    if request.method != 'POST':
        return HttpResponseBadRequest(json.dumps({'message': 'bad request'}), content_type='application/json')
    try:
        req_body = json.loads(request.body)
        note = req_body['note']
        job_id = req_body['job_id']
        new_note = Note(
            candidate_id=candidate_id,
            note=note,
            job_id=job_id
        )
        new_note.save()
        response = json.dumps(model_to_dict(new_note))
        return HttpResponse(response, content_type='application/json', status=201)

    except:
        return HttpResponseBadRequest(json.dumps({'message': 'bad request'}), content_type='application/json')
