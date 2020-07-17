package parser

import (
	"db-puller/avro_writer"
	"db-puller/schema"
)

func parseEventToAvroEvent(event schema.Event) (avroSequence avro_writer.AvroEvent) {
	avroSequence.Id = int32(event.Id)
	avroSequence.XCoordinate = int32(event.XCoordinate)
	avroSequence.YCoordinate = int32(event.YCoordinate)
	avroSequence.XResolution = int32(event.XResolution)
	avroSequence.YResolution = int32(event.YResolution)
	return
}

func ParseEventsToAvroEvents(events []schema.Event) (avroEvents []*avro_writer.AvroEvent) {
	for _, el := range events {
		parsedElement := parseEventToAvroEvent(el)
		avroEvents = append(avroEvents, &parsedElement)
	}
	return
}