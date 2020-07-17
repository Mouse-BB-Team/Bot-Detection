package avro_writer

import (
	"bytes"
	"db-puller/utils"
	"gopkg.in/avro.v0"
	"os"
)

type Writer interface {
	Write(sequence *AvroUser, filepath string)
}

type avroWriter struct {
	writer  *avro.DatumWriter
}

func NewWriter(schemaPath string) *avroWriter {
	schema, err := avro.ParseSchemaFile(schemaPath)
	utils.HandleError(err)
	datumWriter := avro.NewSpecificDatumWriter().SetSchema(schema)
	return &avroWriter{writer: &datumWriter}
}

func (writer *avroWriter) Write(sequence *AvroUser, filepath string) {
	writtenBytes := writeToBuffer(writer.writer, sequence)
	saveToFile(writtenBytes, filepath)
}

func writeToBuffer(writer *avro.DatumWriter, sequence *AvroUser) (writerBuffer *bytes.Buffer){
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