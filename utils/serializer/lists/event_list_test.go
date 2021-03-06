package lists

import (
	"github.com/Mouse-BB-Team/Bot-Detection/utils/serializer/schema"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"testing"
	"time"
)

func prepareEventList() (eventList []schema.Event, firstSequence []schema.Event, secondSequence []schema.Event) {
	firstSequenceTime := time.Now()
	firstSequence = getEventsForIds([]int{1, 2, 3, 4, 5}, schema.EventType{Id: 1}, firstSequenceTime, time.Millisecond*900)
	secondSequenceTime := firstSequenceTime.Add(6 * time.Second)
	secondSequence = getEventsForIds([]int{1, 2, 3}, schema.EventType{Id: 1}, secondSequenceTime, time.Millisecond*900)
	eventList = append(eventList, firstSequence...)
	eventList = append(eventList, secondSequence...)
	return
}

func getEventsForIds(ids []int, eventType schema.EventType, beginTime time.Time, delayBetweenEvents time.Duration) (eventList []schema.Event) {
	for i := range ids {
		eventList = append(eventList, schema.Event{
			Id:          int64(i),
			EventId:     eventType.Id,
			EventTime:   beginTime.Add(delayBetweenEvents),
			XResolution: 1280,
			YResolution: 800,
		})
	}
	return
}

func TestSequence_Split(t *testing.T) {
	t.Run("should split event list into array of lists", func(t *testing.T) {
		events, firstSequence, secondSequence := prepareEventList()

		eventList := EventList{eventList: events}

		args := SplitArgs{
			RequiredEventType:     schema.EventType{Id: 1},
			GapSeconds:            1.0,
			MinimumSequenceLength: 1,
			MinimumXResolution:    1280,
			MinimumYResolution:    800,
		}

		splitted := eventList.Split(args)

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
		sequence := EventList{eventList: make([]schema.Event, 5)}
		expectedLength := 10

		require.True(t, isPreviousSequenceToShort(&sequence, expectedLength))
	})

	t.Run("should return that sequence is to short", func(t *testing.T) {
		sequence := EventList{eventList: make([]schema.Event, 10)}
		expectedLength := 10

		require.False(t, isPreviousSequenceToShort(&sequence, expectedLength))
	})
}

func Test_isRequiredEvent(t *testing.T) {
	t.Run("should return that event is required", func(t *testing.T) {
		testEvent := schema.Event{EventId: 1}
		expectedEventType := schema.EventType{Id: 1}

		require.True(t, isRequiredEvent(testEvent, expectedEventType))
	})

	t.Run("should return that event is not required", func(t *testing.T) {
		testEvent := schema.Event{EventId: 1}
		expectedEventType := schema.EventType{Id: 2}

		require.False(t, isRequiredEvent(testEvent, expectedEventType))
	})
}

func Test_isRequiredScreenResolution(t *testing.T) {
	t.Run("should return that resolution is not proper", func(t *testing.T) {
		xRes, yRes := 1280, 800
		event := schema.Event{XResolution: xRes, YResolution: yRes}

		xRes = 3000
		assert.False(t, isRequiredScreenResolution(event, xRes, yRes))
	})

	t.Run("should return that resolution is proper", func(t *testing.T) {
		xRes, yRes := 1280, 800
		event := schema.Event{XResolution: xRes, YResolution: yRes}

		assert.True(t, isRequiredScreenResolution(event, xRes, yRes))
	})
}
