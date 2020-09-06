import json

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from api.candidate.models import Note
from .models import Job, JOB_STATUS_CHOICES, Opinion


def get_stats(request, job_id):
    if request.method != 'GET':
        return HttpResponseBadRequest(json.dumps({'message': 'bad request'}), content_type='application/json')
    try:
        opinions = Opinion.objects.filter(job_id=job_id)
        liked = opinions.filter(liked=True).values('liked').annotate(total=Count('liked')).first()
        disliked = opinions.filter(liked=False).values('liked').annotate(total=Count('liked')).first()
        notes = Note.objects.filter(job_id=job_id).values('candidate_id').annotate(total=Count('candidate_id')).all()
        response = {
            'likes': liked['total'],
            'dislikes': disliked['total'],
            'notes': list(notes)
        }
        print(response)
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(json.dumps({'message': 'not found'}), content_type='application/json')


@csrf_exempt
def update_status(request, job_id):
    if request.method != 'PUT':
        return HttpResponseBadRequest(json.dumps({'message': 'bad request'}), content_type='application/json')
    try:
        body = json.loads(request.body)
        status_value = body['status'].upper()
        if status_value not in [c[0] for c in JOB_STATUS_CHOICES]:
            raise ValidationError('invalid status value')
        job_obj = Job.objects.get(id=job_id)
        job_obj.status = status_value
        job_obj.save()
        response = json.dumps(model_to_dict(job_obj))
        return HttpResponse(response, content_type='application/json')
    except ValidationError as e:
        return HttpResponseNotFound(json.dumps({'message': e.message}), content_type='application/json')
