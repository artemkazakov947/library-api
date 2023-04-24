import stripe
from rest_framework.exceptions import APIException

import library_api.settings
from borrowing.models import Borrowing


stripe.api_key = library_api.settings.STRIPE_SECRET_KEY


def stripe_session(borrowing: Borrowing, payment_id: int):
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
                            "name": borrowing.book.title,
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"http://127.0.0.1:8000/api/payments/{payment_id}/success",
            cancel_url=f"http://127.0.0.1:8000/api/payments/{payment_id}/cancel",
        )

        return session
    except Exception as e:
        raise APIException({"error": f"{e}. Creation of payment session failed"})

