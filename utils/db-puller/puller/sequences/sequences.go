package sequences

import (
	"db-puller/puller/schema/event"
	"time"
)

type SequenceList struct {
	sequenceList []*Sequence
}

func (sequenceList *SequenceList) Get() []*Sequence {
	return sequenceList.sequenceList
}

func (sequenceList *SequenceList) Append(sequence *Sequence) {
	sequenceList.sequenceList = append(sequenceList.sequenceList, sequence)
}

func (sequenceList *SequenceList) set(sequences []*Sequence)  {
	sequenceList.sequenceList = sequences
}

type Sequence struct {
	eventList []event.Event
}

func (events *Sequence) Get() []event.Event {
	return events.eventList
}

func (events *Sequence) Append(event event.Event) {
	events.eventList = append(events.eventList, event)
}

func (events *Sequence) Set(eventList []event.Event) {
	events.eventList = eventList
}

func (events *Sequence) Split(requiredEventType event.EventType, gapSeconds float64, minimumSequenceLength int) (splittedSequences *SequenceList) {
	var currentSequence = new(Sequence)

	splittedSequences = new(SequenceList)
	splittedSequences.Append(currentSequence)

	var previousEvent = event.InitialEmptyEvent()

	for _, e := range events.Get() {
		if isRequiredEvent(e, requiredEventType) {
			if isBeginOfNewSequence(previousEvent.EventTime, e.EventTime, gapSeconds) {
				if isPreviousSequenceToShort(currentSequence, minimumSequenceLength) {
					splittedSequences.dropLastItem()
				}
				currentSequence = new(Sequence)
				splittedSequences.Append(currentSequence)
			}

			currentSequence.Append(e)
			previousEvent = e
		}
	}

	return
}

func (sequenceList *SequenceList) len() int{
	return len(sequenceList.sequenceList)
}

func (sequenceList *SequenceList) dropLastItem(){
	sequenceList.sequenceList = sequenceList.sequenceList[:sequenceList.len() - 1]
}

func isRequiredEvent(event event.Event, eventType event.EventType) bool{
	return event.EventId == eventType.Id
}

func isPreviousSequenceToShort(sequence *Sequence, length int) bool{
	return len(sequence.eventList) < length
}

func isBeginOfNewSequence(prev time.Time, curr time.Time, delayGap float64) bool {
	if !prev.IsZero() {
		return curr.Sub(prev).Seconds() > delayGap
	} else {
		return false
	}
}