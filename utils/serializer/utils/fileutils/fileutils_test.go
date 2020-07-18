package fileutils

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"math/rand"
	"os"
	"reflect"
	"serializer/consts"
	"serializer/utils"
	"testing"
)

func TestCreateDir(t *testing.T) {
	t.Run("should create dir with given path", func(t *testing.T) {
		random := rand.Uint32()
		tmpDir := os.TempDir()
		dirName := fmt.Sprintf("test-dir-%d", random)
		createdDirPath := CreateDir(dirName, tmpDir)

		require.Equal(t, tmpDir+"/"+dirName, createdDirPath)
		require.DirExists(t, createdDirPath)

		cleanUp(createdDirPath)
	})
}

func TestCreateUserDir(t *testing.T) {
	t.Run("should create dir for given user", func(t *testing.T) {
		random := rand.Uint32()
		tmpDir := os.TempDir()
		expectedDirPath := fmt.Sprintf("%s/%s-%d", tmpDir, consts.OutputUserDirPrefix, random)

		createdDirPath := CreateUserDir(int64(random), tmpDir)

		require.Equal(t, expectedDirPath, createdDirPath)
		require.DirExists(t, createdDirPath)

		cleanUp(createdDirPath)
	})
}

func TestSaveToFile(t *testing.T) {
	t.Run("should write bytes to file", func(t *testing.T) {
		random := rand.Uint32()
		bytesSaved := make([]byte, 4)
		binary.LittleEndian.PutUint32(bytesSaved, random)
		buffer := bytes.NewBuffer(bytesSaved)

		rootDir := createTestDir(random)
		defer cleanUp(rootDir)

		filepath := getFileNameWith(rootDir, random)
		SaveToFile(buffer.Bytes(), filepath)

		f, err := os.Open(filepath)
		utils.HandleError(err)
		defer f.Close()

		bytesRead := make([]byte, 4)
		_, err = f.Read(bytesRead)
		utils.HandleError(err)

		assert.True(t, reflect.DeepEqual(bytesRead, bytesSaved))
	})
}

func Test_getFilePathWith(t *testing.T) {
	t.Run("should return proper file path for provided arguments", func(t *testing.T) {
		usrId := 1
		seqId := 2
		path := "/tmp"
		expectedPath := fmt.Sprintf("%s/%s-%d-%s-%d", path, consts.OutputFileSequencePrefix, seqId, consts.OutputFileUserPrefix, usrId)
		gotPath := getFilePathWith(int64(usrId), seqId, path)

		assert.Equal(t, expectedPath, gotPath)
	})
}

func createTestDir(randomInt uint32) string {
	tempDir := os.TempDir()
	dirPath := fmt.Sprintf("%s/test-dir-%d/", tempDir, randomInt)
	err := os.Mkdir(dirPath, os.ModePerm)
	utils.HandleError(err)
	return dirPath
}

func cleanUp(path string) {
	err := os.RemoveAll(path)
	utils.HandleError(err)
}

func getFileNameWith(rootDir string, randomInt uint32) string {
	return fmt.Sprintf("%s/test-file-%d", rootDir, randomInt)
}
