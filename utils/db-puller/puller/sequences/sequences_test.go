package sequences

import (
	"db-puller/puller/schema/event"
	"testing"
)

//func TestSequenceList_dropLastItem(t *testing.T) {
//	tests := []struct {
//		name         string
//		sequenceList SequenceList
//		want         *SequenceList
//	}{
//		// TODO: Add test cases.
//	}
//	for _, tt := range tests {
//		t.Run(tt.name, func(t *testing.T) {
//			if got := tt.sequenceList.dropLastItem(); !reflect.DeepEqual(got, tt.want) {
//				t.Errorf("dropLastItem() = %v, want %v", got, tt.want)
//			}
//		})
//	}
//}
//
//func TestSequenceList_len(t *testing.T) {
//	tests := []struct {
//		name         string
//		sequenceList SequenceList
//		want         int
//	}{
//		// TODO: Add test cases.
//	}
//	for _, tt := range tests {
//		t.Run(tt.name, func(t *testing.T) {
//			if got := tt.sequenceList.len(); got != tt.want {
//				t.Errorf("len() = %v, want %v", got, tt.want)
//			}
//		})
//	}
//}
//
//func TestSequence_Split(t *testing.T) {
//	type args struct {
//		requiredEventType     event.EventType
//		gapSeconds            float64
//		minimumSequenceLength int
//	}
//	tests := []struct {
//		name                  string
//		events                Sequence
//		args                  args
//		wantSplittedSequences *SequenceList
//	}{
//		// TODO: Add test cases.
//	}
//	for _, tt := range tests {
//		t.Run(tt.name, func(t *testing.T) {
//			if gotSplittedSequences := tt.events.Split(tt.args.requiredEventType, tt.args.gapSeconds, tt.args.minimumSequenceLength); !reflect.DeepEqual(gotSplittedSequences, tt.wantSplittedSequences) {
//				t.Errorf("Split() = %v, want %v", gotSplittedSequences, tt.wantSplittedSequences)
//			}
//		})
//	}
//}
//
//func Test_isBeginOfNewSequence(t *testing.T) {
//	type args struct {
//		prev     time.Time
//		curr     time.Time
//		delayGap float64
//	}
//	tests := []struct {
//		name string
//		args args
//		want bool
//	}{
//		// TODO: Add test cases.
//	}
//	for _, tt := range tests {
//		t.Run(tt.name, func(t *testing.T) {
//			if got := isBeginOfNewSequence(tt.args.prev, tt.args.curr, tt.args.delayGap); got != tt.want {
//				t.Errorf("isBeginOfNewSequence() = %v, want %v", got, tt.want)
//			}
//		})
//	}
//}
//
func Test_isPreviousSequenceToShort(t *testing.T) {
	type args struct {
		sequence *Sequence
		length   int
	}
	tests := []struct {
		name string
		args args
		want bool
	}{
		{
			name: "should return that sequence is to short",
			args: args{
				sequence: &(Sequence{eventList: make([]event.Event, 5)}),
				length: 10,
			},
			want: true,
		},
		{
			name: "should return that sequence has required minimum length",
			args: args{
				sequence: &(Sequence{eventList: make([]event.Event, 10)}),
				length: 10,
			},
			want: false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := isPreviousSequenceToShort(tt.args.sequence, tt.args.length); got != tt.want {
				t.Errorf("isPreviousSequenceToShort() = %v, want %v", got, tt.want)
			}
		})
	}
}

func Test_isRequiredEvent(t *testing.T) {
	type args struct {
		event     event.Event
		eventType event.EventType
	}
	tests := []struct {
		name string
		args args
		want bool
	}{
		{
			name: "should return that event is required",
			args: args{
				event: event.Event{EventId: 1},
				eventType: event.EventType{Id: 1},
			},
			want: true,
		},
		{
			name: "should return that event is not required",
			args: args{
				event: event.Event{EventId: 1},
				eventType: event.EventType{Id: 2},
			},
			want: false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := isRequiredEvent(tt.args.event, tt.args.eventType); got != tt.want {
				t.Errorf("isRequiredEvent() = %v, want %v", got, tt.want)
			}
		})
	}
}