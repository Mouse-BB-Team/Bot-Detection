package sequences

import (
	"db-puller/puller/schema/event"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"testing"
)

func TestSequenceList_Append(t *testing.T) {
	array := make([]*EventList, 5)
	basicLength := len(array)
	sequenceList := SequenceList{sequenceList: array}
	elementToAppend := EventList{eventList: make([]event.Event, 2)}
	sequenceList.Append(&elementToAppend)

	require.Len(t, sequenceList.sequenceList, 6)

	for i := 0; i < basicLength; i++ {
		require.Same(t, array[i], sequenceList.sequenceList[i])
	}

	require.Same(t, &elementToAppend, sequenceList.sequenceList[basicLength])
}

func TestSequenceList_DropLastItem(t *testing.T) {
	t.Run("should drop last item from inner array", func(t *testing.T) {
		array := make([]*EventList, 5)
		sequenceList := SequenceList{sequenceList: array}
		want := array[:len(array)-1]

		sequenceList.DropLastItem()
		got := sequenceList.sequenceList

		require.ElementsMatch(t, want, got)

		for i := 0; i < len(want); i++ {
			require.Same(t, want[i], got[i])
		}
	})
}

func TestSequenceList_Get(t *testing.T) {
	t.Run("should get array from sequenceList struct", func(t *testing.T) {
		want := make([]*EventList, 5)
		sequenceList := SequenceList{want}
		got := sequenceList.Get()

		assert.ElementsMatch(t, want, got)

		for i := 0; i < len(want); i++ {
			assert.Same(t, want[i], got[i])
		}
	})
}

func TestSequenceList_Len(t *testing.T) {
	t.Run("should return proper got of sequenceList", func(t *testing.T) {
		sequenceList := SequenceList{make([]*EventList, 10)}
		got := sequenceList.Len()

		assert.Equal(t, 10, got)
	})
}

func TestSequenceList_Set(t *testing.T) {
	t.Run("should set array in sequenceList struct", func(t *testing.T) {
		want := make([]*EventList, 5)
		for i := range want {
			want[i] = new(EventList)
		}
		sequenceList := SequenceList{}
		sequenceList.Set(want)
		got := sequenceList.sequenceList

		require.ElementsMatch(t, want, got)

		for i := 0; i < len(want); i++ {
			require.Same(t, want[i], got[i])
		}
	})
}
