package main

import (
	"db-puller/cmd"
	"db-puller/lists"
	"db-puller/puller"
	"db-puller/schema"
	"fmt"
	"github.com/go-pg/pg"
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

	dbPuller.Pull(splitArgs, *args.InfoRequired)
}
