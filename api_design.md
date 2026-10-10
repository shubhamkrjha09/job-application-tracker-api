GET /applications -> 200 -> see all applications
POST /applications -> 201 -> add a new application
GET /applications/{id} -> 200 -> see one application
PATCH /applications/{id} -> 200 -> change status of one application
DELETE /applications/{id} -> 200 -> delete one application

Errors:
GET /applications/{id} ->404 ->if id doesnot exist
PATCH /applications/{id} ->404 ->if id doesnot exist
DELETE /applications/{id} ->404 ->if id doesnot exist
POST /applications ->422->if company or role is empty


