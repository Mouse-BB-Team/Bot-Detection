package avro_writer

import (
	"bytes"
	"db-puller/utils"
	"encoding/binary"
	"fmt"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"gopkg.in/avro.v0"
	"math/rand"
	"os"
	"reflect"
	"strconv"
	"testing"
)

const DefaultSchemaPath = "../../../config/avro_schema.json"

func TestNewWriter(t *testing.T) {
	t.Run("should return AvroWriter with set DatumWriter inside structure", func(t *testing.T) {
		writer := NewWriter(DefaultSchemaPath)
		require.NotNil(t, writer.writer)
	})

	t.Run("should fail because path is wrong", func(t *testing.T) {
		assert.Panics(t, func() {
			NewWriter(generateNoExistingFilename())
		})
	})
}

func Test_saveToFile(t *testing.T) {
	t.Run("should write bytes to file", func(t *testing.T) {
		random := rand.Uint32()
		bytesSaved := make([]byte, 4)
		binary.LittleEndian.PutUint32(bytesSaved, random)
		buffer := bytes.NewBuffer(bytesSaved)

		rootDir := createTestDir(random)
		defer cleanUp(rootDir)

		filepath := getFileNameWith(rootDir, random)
		saveToFile(buffer, filepath)

		f, err := os.Open(filepath)
		utils.HandleError(err)
		defer f.Close()

		bytesRead := make([]byte, 4)
		_, err = f.Read(bytesRead)
		utils.HandleError(err)

		assert.True(t, reflect.DeepEqual(bytesRead, bytesSaved))
	})
}

func Test_writeToBuffer(t *testing.T) {
	t.Run("should save structure as avro bytes to buffer", func(t *testing.T) {

		events := make([]*SequenceEvent, 1)
		events[0] = &SequenceEvent{
			Id: 3,
			XCoordinate: 4,
			YCoordinate: 5,
			XResolution: 6,
			YResolution: 7,
		}

		savedStructure := &UserSequence{
			Id: 1,
			SequenceId: 2,
			Events: events,
			SequenceLength: 8,
		}

		schema, err := avro.ParseSchemaFile(DefaultSchemaPath)
		utils.HandleError(err)

		writer := avro.NewSpecificDatumWriter().SetSchema(schema)

		buffer := writeToBuffer(&writer, savedStructure)

		decoder := avro.NewBinaryDecoder(buffer.Bytes())

		reader := avro.NewSpecificDatumReader()
		reader.SetSchema(schema)

		readStructure := new(UserSequence)

		err = reader.Read(readStructure, decoder)
		utils.HandleError(err)

		assert.True(t, reflect.DeepEqual(savedStructure, readStructure))
	})
}

func createTestDir(randomInt uint32) string{
	tempDir := os.TempDir()
	dirPath := fmt.Sprintf("%s/test-dir-%d/", tempDir, randomInt)
	err := os.Mkdir(dirPath, os.ModePerm)
	utils.HandleError(err)
	return dirPath
}

func getFileNameWith(rootDir string, randomInt uint32) string {
	return fmt.Sprintf("%s/test-file-%d", rootDir, randomInt)
}

func cleanUp(path string) {
	err := os.RemoveAll(path)
	utils.HandleError(err)
}

func generateNoExistingFilename() (filepath string) {
	for {
		filepath = strconv.Itoa(rand.Int())
		if !ifFileExists(filepath) {
			break
		}
	}
	return
}

func ifFileExists(filepath string)  bool {
	f, err := os.Open(filepath)
	if err == nil {
		return false
	} else {
		err := f.Close()
		utils.HandleError(err)
		return true
	}
}