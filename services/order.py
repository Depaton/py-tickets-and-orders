from datetime import datetime

from django.db import transaction

from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = datetime.strptime(
                date, "%Y-%m-%d %H:%M"
            )
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=order,
            )
    return order


def get_orders(username: str = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all().order_by("-user")
