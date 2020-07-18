package protoparser

import (
	"serializer/proto"
	"serializer/schema"
)

func parseEventToProtoEvent(event schema.Event) (protoEvent protoschema.Event) {
	protoEvent.Id = int32(event.Id)
	protoEvent.XCoordinate = int32(event.XCoordinate)
	protoEvent.YCoordinate = int32(event.YCoordinate)
	protoEvent.XResolution = int32(event.XResolution)
	protoEvent.YResolution = int32(event.YResolution)
	return
}

func parseEventsToProtoEvents(events []schema.Event) (protoEvents []*protoschema.Event) {
	for _, el := range events {
		parsedElement := parseEventToProtoEvent(el)
		protoEvents = append(protoEvents, &parsedElement)
	}
	return
}

func ParseToUserSequence(user schema.User, sequenceId int, events []schema.Event) (userSequence *protoschema.UserSequence) {
	userSequence = &protoschema.UserSequence{
		UserId:         int32(user.Id),
		SequenceId:     int32(sequenceId),
		Events:         parseEventsToProtoEvents(events),
		SequenceLength: int32(len(events)),
	}
	return
}
