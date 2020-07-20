package lists

import (
	"github.com/Mouse-BB-Team/Bot-Detection/utils/serializer/schema"
	"time"
)

type SplitArgs struct {
	RequiredEventType     schema.EventType
	GapSeconds            float64
	MinimumSequenceLength int
	MinimumXResolution    int
	MinimumYResolution    int
}

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

func (events *EventList) Split(args SplitArgs) (splittedSequences *SequenceList) {
	var eventList = new(EventList)
	var previousEvent = schema.InitialEmptyEvent()

	splittedSequences = new(SequenceList)

	for _, e := range events.Get() {
		if isRequiredEvent(e, args.RequiredEventType) && isRequiredScreenResolution(e, args.MinimumXResolution, args.MinimumYResolution) {
			if isBeginOfNewSequence(previousEvent.EventTime, e.EventTime, args.GapSeconds) {
				if !isPreviousSequenceToShort(eventList, args.MinimumSequenceLength) {
					splittedSequences.Append(eventList)
				}
				eventList = new(EventList)
			}

			eventList.Append(e)
			previousEvent = e
		}
	}

	if !isPreviousSequenceToShort(eventList, args.MinimumSequenceLength) {
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

func isRequiredScreenResolution(event schema.Event, minX, minY int) bool {
	return event.XResolution >= minX && event.YResolution >= minY
}
