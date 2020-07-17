package avro_writer

type UserSequence struct {
	Id             int32            `avro:"userId"`
	SequenceId     int32            `avro:"sequenceId"`
	Events         []*SequenceEvent `avro:"events"`
	SequenceLength int32            `avro:"sequenceLength"`
}

type SequenceEvent struct {
	Id          int32 `avro:"id"`
	XCoordinate int32 `avro:"xCoordinate"`
	YCoordinate int32 `avro:"yCoordinate"`
	XResolution int32 `avro:"xResolution"`
	YResolution int32 `avro:"yResolution"`
}
