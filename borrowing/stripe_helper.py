import stripe
from decimal import Decimal
from rest_framework.response import Response
from rest_framework import status

import library_api.settings
from borrowing.models import Borrowing


stripe.api_key = library_api.settings.STRIPE_SECRET_KEY


def stripe_session(borrowing: Borrowing):
    money = (borrowing.expected_return_date - borrowing.borrow_date).days * borrowing.book.daily_fee
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(money.amount * 100),
                        "product_data": {
                            "title": borrowing.book.title,
                            "author": borrowing.book.author,
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://localhost:8000/succsess",
            cancel_url="http://localhost:8000/cancel",
        )

        return session
    except Exception as e:
        return Response({'error': f"{e}"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

