package lists

import (
	"db-puller/schema"
	"time"
)

type EventList struct {
	eventList []schema.Event
}

func (events *EventList) Get() []schema.Event {
	return events.eventList
}

func (events *EventList) Append(event schema.Event) {
	events.eventList = append(events.eventList, event)
}

func (events *EventList) Set(eventList []schema.Event) {
	events.eventList = eventList
}

func (events *EventList) Split(requiredEventType schema.EventType, gapSeconds float64, minimumSequenceLength int) (splittedSequences *SequenceList) {
	var eventList = new(EventList)
	var previousEvent = schema.InitialEmptyEvent()

	splittedSequences = new(SequenceList)

	for _, e := range events.Get() {
		if isRequiredEvent(e, requiredEventType) {
			if isBeginOfNewSequence(previousEvent.EventTime, e.EventTime, gapSeconds) {
				if !isPreviousSequenceToShort(eventList, minimumSequenceLength) {
					splittedSequences.Append(eventList)
				}
				eventList = new(EventList)
			}

			eventList.Append(e)
			previousEvent = e
		}
	}

	if !isPreviousSequenceToShort(eventList, minimumSequenceLength) {
		splittedSequences.Append(eventList)
	}

	return
}

func isRequiredEvent(event schema.Event, eventType schema.EventType) bool {
	return event.EventId == eventType.Id
}

func isPreviousSequenceToShort(sequence *EventList, length int) bool {
	return len(sequence.eventList) < length
}

func isBeginOfNewSequence(prev time.Time, curr time.Time, delayGap float64) bool {
	if !prev.IsZero() {
		return curr.Sub(prev).Seconds() > delayGap
	} else {
		return false
	}
}
