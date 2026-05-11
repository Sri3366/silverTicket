import random
from django.utils import timezone
from .models import Batch, Submission

def get_or_create_batch():
    batch = Batch.objects.filter(status='open').first()

    if not batch:
        last = Batch.objects.order_by('-batch_number').first()
        num = 1 if not last else last.batch_number + 1
        batch = Batch.objects.create(batch_number=num)

    return batch


def assign_ticket(submission):
    batch = get_or_create_batch()

    ticket_number = batch.approved_count + 1

    submission.batch = batch
    submission.ticket_number = ticket_number
    submission.status = 'approved'
    submission.save()

    batch.approved_count += 1

    if batch.approved_count >= 3:
        batch.status = 'full'

    batch.save()


def draw_winner(batch):
    tickets = Submission.objects.filter(batch=batch, status='approved')

    winner = random.choice(list(tickets))

    batch.winner_name = winner.full_name
    batch.winner_ticket_number = winner.ticket_number
    batch.status = 'drawn'
    batch.drawn_at = timezone.now()
    batch.save()

    return batch