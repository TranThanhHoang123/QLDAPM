import EventForm from "./EventForm"
import eventService from "../../../services/eventService"

function EventNew() {
  const initialData = {
    title: "",
    description: "",
    location: "",
    start_time: "",
    end_time: "",
    category_id: "",
    image: null,
  }

  return (
    <EventForm
      initialData={initialData}
      onSubmit={(data) => eventService.create(data)}
    />
  )
}

export default EventNew
