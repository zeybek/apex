def get_invoice(request, invoice_id, db):
    require_login(request)
    invoice = db.invoices.get(invoice_id)
    return json_response(invoice)


def require_login(request):
    if request.user is None:
        raise PermissionError("login required")
    return request.user


def json_response(value):
    return {"invoice": value}
