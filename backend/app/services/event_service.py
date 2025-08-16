from app.extensions import db
from app.models import Event
from datetime import datetime
class EventService:
    def get_events(self, **kwargs):
        query = Event.query

        # Tìm theo tiêu đề
        if "title" in kwargs and kwargs["title"]:
            query = query.filter(Event.title.ilike(f"%{kwargs['title']}%"))

        # Tìm theo địa điểm
        if "location" in kwargs and kwargs["location"]:
            query = query.filter(Event.location.ilike(f"%{kwargs['location']}%"))

        # Tìm theo thời gian bắt đầu (>=)
        if "start_time" in kwargs and kwargs["start_time"]:
            query = query.filter(Event.start_time >= kwargs["start_time"])

        # Tìm theo thời gian kết thúc (<=)
        if "end_time" in kwargs and kwargs["end_time"]:
            query = query.filter(Event.end_time <= kwargs["end_time"])

        # Tìm theo category
        if "category_id" in kwargs and kwargs["category_id"]:
            query = query.filter(Event.category_id == kwargs["category_id"])


        # Phân trang
        try:
            page = int(kwargs.get("page", 1))
        except ValueError:
            page = 1

        try:
            page_size = int(kwargs.get("page_size", 10))
        except ValueError:
            page_size = 10

        pagination = query.paginate(page=page, per_page=page_size, error_out=False)
        return pagination

    def get_event(self, event_id):
        return Event.query.get(event_id)
    
    def create_event(self, **data):
        # Convert string -> datetime nếu truyền vào là string
        if isinstance(data.get("start_time"), str):
            data["start_time"] = datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S")
        if isinstance(data.get("end_time"), str):
            data["end_time"] = datetime.strptime(data["end_time"], "%Y-%m-%d %H:%M:%S")

        event = Event(**data)
        db.session.add(event)
        db.session.commit()
        return event

    def delete_event(self, event_id):
        event = Event.query.filter(
            Event.id == event_id,
        ).first()
        
        if not event:
            return False
        
        db.session.delete(event)
        db.session.commit()
        return True


    def update_event(self, event_id, **data):
        event = Event.query.get(event_id)
        if not event:
            raise ValueError("Event not found")

        if isinstance(data.get("start_time"), str):
            data["start_time"] = datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S")
        if isinstance(data.get("end_time"), str):
            data["end_time"] = datetime.strptime(data["end_time"], "%Y-%m-%d %H:%M:%S")

        # cập nhật các field
        for key, value in data.items():
            setattr(event, key, value)

        db.session.commit()
        return event
