package sequences

import (
	"db-puller/puller/schema/event"
	"github.com/stretchr/testify/require"
	"testing"
	"time"
)

func prepareEventList() (eventList []event.Event, firstSequence []event.Event, secondSequence []event.Event) {
	firstSequenceTime := time.Now()
	firstSequence = getEventsForIds([]int{1, 2, 3, 4, 5}, event.EventType{Id: 1}, firstSequenceTime, time.Millisecond * 900)
	secondSequenceTime := firstSequenceTime.Add(6 * time.Second)
	secondSequence = getEventsForIds([]int{1, 2, 3}, event.EventType{Id: 1}, secondSequenceTime, time.Millisecond * 900)
	eventList = append(eventList, firstSequence...)
	eventList = append(eventList, secondSequence...)
	return
}

func getEventsForIds(ids []int, eventType event.EventType, beginTime time.Time, delayBetweenEvents time.Duration) (eventList []event.Event) {
	for i := range ids {
		eventList = append(eventList, event.Event{
			Id: int64(i),
			EventId: eventType.Id,
			EventTime: beginTime.Add(delayBetweenEvents),
		})
	}
	return
}

func TestSequence_Split(t *testing.T) {
	t.Run("should split event list into array of sequences", func(t *testing.T) {
		events, firstSequence, secondSequence := prepareEventList()

		eventList := EventList{eventList: events}

		splitted := eventList.Split(event.EventType{Id: 1}, 1.0, 1)

		require.ElementsMatch(t, firstSequence, (*splitted).sequenceList[0].eventList)
		require.ElementsMatch(t, secondSequence, (*splitted).sequenceList[1].eventList)
	})
}

func Test_isBeginOfNewSequence(t *testing.T) {
	t.Run("should return that this is not new sequence (gap time equals expected time)", func(t *testing.T) {
		prev := time.Unix(1, 0)
		curr := time.Unix(2, 0)
		delayGap := 1.0

		require.False(t, isBeginOfNewSequence(prev, curr, delayGap))
	})

	t.Run("should return that this is not new sequence (gap time smaller than expected time)", func(t *testing.T) {
		prev := time.Unix(1, 0)
		curr := time.Unix(1, 50)
		delayGap := 1.0

		require.False(t, isBeginOfNewSequence(prev, curr, delayGap))
	})

	t.Run("should return that this is new sequence", func(t *testing.T) {
		prev := time.Unix(1, 0)
		curr := time.Unix(2, 1)
		delayGap := 1.0

		require.True(t, isBeginOfNewSequence(prev, curr, delayGap))
	})
}

func Test_isPreviousSequenceToShort(t *testing.T) {
	t.Run("should return that sequence is to short", func(t *testing.T) {
		sequence := EventList{eventList: make([]event.Event, 5)}
		expectedLength := 10

		require.True(t, isPreviousSequenceToShort(&sequence, expectedLength))
	})

	t.Run("should return that sequence is to short", func(t *testing.T) {
		sequence := EventList{eventList: make([]event.Event, 10)}
		expectedLength := 10

		require.False(t, isPreviousSequenceToShort(&sequence, expectedLength))
	})
}

func Test_isRequiredEvent(t *testing.T) {
	t.Run("should return that event is required", func(t *testing.T) {
		testEvent := event.Event{EventId: 1}
		expectedEventType := event.EventType{Id: 1}

		require.True(t, isRequiredEvent(testEvent, expectedEventType))
	})

	t.Run("should return that event is not required", func(t *testing.T) {
		testEvent := event.Event{EventId: 1}
		expectedEventType := event.EventType{Id: 2}

		require.False(t, isRequiredEvent(testEvent, expectedEventType))
	})
}
