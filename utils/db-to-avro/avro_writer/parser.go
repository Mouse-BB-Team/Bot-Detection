package avro_writer

import (
	"bytes"
	"db-puller/utils"
	"gopkg.in/avro.v0"
	"os"
)

type AvroWriter struct {
	writer  *avro.DatumWriter
}

func NewWriter(schemaPath string) *AvroWriter {
	schema, err := avro.ParseSchemaFile(schemaPath)
	utils.HandleError(err)
	datumWriter := avro.NewSpecificDatumWriter().SetSchema(schema)
	return &AvroWriter{writer:  &datumWriter}
}

func (writer *AvroWriter) Write(sequence *UserSequence, filepath string) {
	writtenBytes := writeToBuffer(writer.writer, sequence)
	saveToFile(writtenBytes, filepath)
}

func writeToBuffer(writer *avro.DatumWriter, sequence *UserSequence) (writerBuffer *bytes.Buffer){
	writerBuffer = new(bytes.Buffer)
	encoder := avro.NewBinaryEncoder(writerBuffer)

	err := (*writer).Write(sequence, encoder)
	utils.HandleError(err)

	return
}

func saveToFile(buffer *bytes.Buffer, filepath string) {
	f, err := os.Create(filepath)
	utils.HandleError(err)

	_, err = f.Write(buffer.Bytes())
	utils.HandleError(err)

	err = f.Close()
	utils.HandleError(err)
}