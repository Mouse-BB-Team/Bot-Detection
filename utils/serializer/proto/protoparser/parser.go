package protoparser

import (
	"serializer/proto"
	"serializer/schema"
)

func parseEventToProtoEvent(event schema.Event) (avroSequence protoschema.Event) {
	avroSequence.Id = int32(event.Id)
	avroSequence.XCoordinate = int32(event.XCoordinate)
	avroSequence.YCoordinate = int32(event.YCoordinate)
	avroSequence.XResolution = int32(event.XResolution)
	avroSequence.YResolution = int32(event.YResolution)
	return
}

func parseEventsToProtoEvents(events []schema.Event) (avroEvents []*protoschema.Event) {
	for _, el := range events {
		parsedElement := parseEventToProtoEvent(el)
		avroEvents = append(avroEvents, &parsedElement)
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
