package sequences

import (
	"db-puller/puller/schema/event"
	"time"
)

type EventList struct {
	eventList []event.Event
}

func (events *EventList) Get() []event.Event {
	return events.eventList
}

func (events *EventList) Append(event event.Event) {
	events.eventList = append(events.eventList, event)
}

func (events *EventList) Set(eventList []event.Event) {
	events.eventList = eventList
}

func (events *EventList) Split(requiredEventType event.EventType, gapSeconds float64, minimumSequenceLength int) (splittedSequences *SequenceList) {
	var eventList = new(EventList)

	splittedSequences = new(SequenceList)
	splittedSequences.Append(eventList)

	var previousEvent = event.InitialEmptyEvent()

	for _, e := range events.Get() {
		if isRequiredEvent(e, requiredEventType) {
			if isBeginOfNewSequence(previousEvent.EventTime, e.EventTime, gapSeconds) {
				if isPreviousSequenceToShort(eventList, minimumSequenceLength) {
					splittedSequences.DropLastItem()
				}
				eventList = new(EventList)
				splittedSequences.Append(eventList)
			}

			eventList.Append(e)
			previousEvent = e
		}
	}

	return
}

func isRequiredEvent(event event.Event, eventType event.EventType) bool{
	return event.EventId == eventType.Id
}

func isPreviousSequenceToShort(sequence *EventList, length int) bool{
	return len(sequence.eventList) < length
}

func isBeginOfNewSequence(prev time.Time, curr time.Time, delayGap float64) bool {
	if !prev.IsZero() {
		return curr.Sub(prev).Seconds() > delayGap
	} else {
		return false
	}
}