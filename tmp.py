from app import delete_entry_by_id,app
with app.app_context():
    delete_entry_by_id(1)