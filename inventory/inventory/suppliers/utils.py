def prepare_suppliers_list(suppliers):
    return [
        {
            "id": supplier.id,
            "name": supplier.name,
            "contact_name": supplier.contact_name,
            "supplier_country": supplier.supplier_country,
            "phone_number": supplier.phone_number,
            "email": supplier.email,
        }
        for supplier in suppliers
    ]
