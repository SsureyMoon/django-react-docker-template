import json

from django.http import HttpResponse

from .aws_handlers import get_sqs_client


def test_send_email(request):
    sc = get_sqs_client()

    sc.send_message(MessageBody=json.dumps({'name': 'SEND_EMAIL', 'to':'smoon@example.com'}))
    return HttpResponse('sending mail to {}'.format('smoon@example.com'), status=200)