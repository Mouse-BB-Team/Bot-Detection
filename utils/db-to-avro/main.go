package main

import (
	"db-puller/cmd"
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
	dbPuller.Pull(schema.EventType{Id: int64(*args.EventTypeId)}, *args.GapTime, *args.MinSequenceLength, *args.InfoRequired)

}
