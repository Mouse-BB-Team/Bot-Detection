package fileutils

import (
	"fmt"
	"github.com/golang/protobuf/proto"
	"log"
	"os"
	"serializer/consts"
	"serializer/proto/protoparser"
	"serializer/schema"
	"serializer/utils"
)

func Serialize(user schema.User, sequenceId int, events []schema.Event, usrDir string) {
	log.Println(fmt.Sprintf("Serializing data for user %d with sequence %d...", user.Id, sequenceId))
	userSequence := protoparser.ParseToUserSequence(user, sequenceId, events)
	marshal, err := proto.Marshal(userSequence)
	utils.HandleError(err)

	SaveToFile(marshal, getFilePathWith(user.Id, sequenceId, usrDir))
	log.Println(fmt.Sprintf("Serialized data for user %d with sequence %d", user.Id, sequenceId))
}

func SaveToFile(buffer []byte, filepath string) {
	f, err := os.Create(filepath)
	utils.HandleError(err)

	_, err = f.Write(buffer)
	utils.HandleError(err)

	err = f.Close()
	utils.HandleError(err)
}

func getFilePathWith(usrId int64, seqId int, path string) string {
	return fmt.Sprintf("%s/%s-%d-%s-%d", path, consts.OutputFileSequencePrefix, seqId, consts.OutputFileUserPrefix, usrId)
}

func CreateUserDir(id int64, path string) string {
	dirName := fmt.Sprintf("%s-%d", consts.OutputUserDirPrefix, id)
	return CreateDir(dirName, path)
}

func CreateDir(name, path string) (dir string) {
	dir = fmt.Sprintf("%s/%s", path, name)
	err := os.Mkdir(dir, os.ModePerm)
	utils.HandleError(err)
	return
}
