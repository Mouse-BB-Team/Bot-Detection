package main

import (
	"fmt"
	"github.com/go-pg/pg"
	"log"
	"serializer/cmd"
	"serializer/consts"
	"serializer/lists"
	"serializer/puller"
	"serializer/schema"
	"serializer/utils/fileutils"
)

func main() {
	log.Println("Starting serializer ...")
	args := cmd.ParseArgs()

	log.Println(fmt.Sprintf("Pulling data from database: %s, as user: %s", *args.DBName, *args.DBUser))

	dbOptions := &pg.Options{
		Addr:     fmt.Sprintf(":%d", *args.DBPort),
		User:     *args.DBUser,
		Password: *args.DBPassword,
		Database: *args.DBName,
	}

	dbPuller := puller.NewDBPuller(dbOptions)
	dbPuller.Connect()
	defer dbPuller.Close()

	splitArgs := lists.SplitArgs{
		RequiredEventType:     schema.EventType{Id: int64(*args.EventTypeId)},
		GapSeconds:            *args.GapTime,
		MinimumSequenceLength: *args.MinSequenceLength,
		MinimumXResolution:    *args.MinXResolution,
		MinimumYResolution:    *args.MinYResolution,
	}

	var sequenceMap *map[schema.User]*lists.SequenceList
	var usersCount, sequencesCount int

	if *args.InfoRequired {
		sequenceMap, usersCount, sequencesCount = dbPuller.Pull(splitArgs)
		log.Println(fmt.Sprintf("Total sequences count %d for %d users", usersCount, sequencesCount))
	} else {
		sequenceMap, _, _ = dbPuller.Pull(splitArgs)
	}

	log.Println("Data has been pulled")

	rootDir := fileutils.CreateDir(consts.OutputDirName, *args.OutputPath)

	for usr, list := range *sequenceMap {
		usrDir := fileutils.CreateUserDir(usr.Id, rootDir)

		for seqId, seq := range list.Get() {
			fileutils.Serialize(usr, seqId, seq.Get(), usrDir)
		}
	}

	log.Println("Serialization complete")
	log.Println(fmt.Sprintf("Data has been saved in: %s", rootDir))
}
