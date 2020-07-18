package main

import (
	"db-puller/avro_writer"
	"db-puller/cmd"
	"db-puller/consts"
	"db-puller/lists"
	"db-puller/parser"
	"db-puller/puller"
	"db-puller/schema"
	"db-puller/utils"
	"fmt"
	"github.com/go-pg/pg"
	"os"
)

func main() {
	args := cmd.ParseArgs()

	dbOptions := &pg.Options{
		Addr:     fmt.Sprintf(":%d", *args.DBPort),
		User:     *args.DBUser,
		Password: *args.DBPassword,
		Database: *args.DBName,
	}

	dbPuller := puller.Puller{Options: dbOptions}
	dbPuller.Connect()
	defer dbPuller.Close()

	splitArgs := lists.SplitArgs{
		RequiredEventType: schema.EventType{Id: int64(*args.EventTypeId)},
		GapSeconds: *args.GapTime,
		MinimumSequenceLength: *args.MinSequenceLength,
		MinimumXResolution: *args.MinXResolution,
		MinimumYResolution: *args.MinYResolution,
	}

	sequenceMap := dbPuller.Pull(splitArgs, *args.InfoRequired)

	fileWriter := avro_writer.NewWriter(consts.DefaultSchemaPath)

	rootDir := createDir(consts.OutputDirName, *args.OutputPath)

	for usr, list := range *sequenceMap {
		usrDir := createUserDir(usr.Id, rootDir)

		for i, seq := range list.Get() {
			events := parser.ParseEventsToAvroEvents(seq.Get())

			avroUser := &avro_writer.AvroUser{
				Id: int32(usr.Id),
				SequenceId: int32(i),
				Events: events,
				SequenceLength: int32(len(events)),
			}

			fileWriter.Write(avroUser, getFileNameWith(usr.Id, i, usrDir))
		}
	}
}

func getFileNameWith(usrId int64, seqId int, path string) string {
	return fmt.Sprintf("%s/%s-%d-%s-%d", path, consts.OutputFileSequencePrefix, seqId, consts.OutputFileUserPrefix, usrId)
}

func createUserDir(id int64, path string) string {
	dirName := fmt.Sprintf("%s-%d", consts.OutputUserDirPrefix, id)
	return createDir(dirName, path)
}

func createDir(name, path string) (dir string) {
	dir = fmt.Sprintf("%s/%s/", path, name)
	err := os.Mkdir(dir, os.ModePerm)
	utils.HandleError(err)
	return
}