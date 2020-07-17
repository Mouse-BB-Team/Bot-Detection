package avro_writer

type AvroUser struct {
	Id             int32        `avro:"userId"`
	SequenceId     int32        `avro:"sequenceId"`
	Events         []*AvroEvent `avro:"events"`
	SequenceLength int32        `avro:"sequenceLength"`
}

type AvroEvent struct {
	Id          int32 `avro:"id"`
	XCoordinate int32 `avro:"xCoordinate"`
	YCoordinate int32 `avro:"yCoordinate"`
	XResolution int32 `avro:"xResolution"`
	YResolution int32 `avro:"yResolution"`
}
