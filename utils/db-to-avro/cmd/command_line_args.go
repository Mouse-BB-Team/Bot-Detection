package cmd

import (
	"db-puller/consts"
	"flag"
)

type Args struct {
	GapTime           *float64
	MinSequenceLength *int
	InfoRequired      *bool
	DBPort            *int
	DBUser            *string
	DBPassword        *string
	DBName            *string
	EventTypeId       *int
	MinXResolution    *int
	MinYResolution    *int
}

func ParseArgs() (args Args) {
	args.GapTime = flag.Float64("gap-delay", 1.0, "gap between lists")
	args.MinSequenceLength = flag.Int("min-seq-length", 10, "minimal sequence length")
	args.InfoRequired = flag.Bool("verbose", false, "if *true* print info about processed data")
	args.DBPort = flag.Int("db-port", consts.DefaultDatabasePort, "database port")
	args.DBName = flag.String("db-name", consts.DefaultDatabaseName, "database name")
	args.DBUser = flag.String("db-user", consts.DefaultDatabaseUser, "database user")
	args.DBPassword = flag.String("db-password", consts.DefaultDatabasePassword, "database password")
	args.EventTypeId = flag.Int("event-type", consts.DefaultEventTypeId, "event type id")
	args.MinXResolution = flag.Int("min-x-resolution", consts.DefaultMinXResolution, "minimum x screen resolution")
	args.MinYResolution = flag.Int("min-y-resolution", consts.DefaultMinYResolution, "minimum y screen resolution")
	flag.Parse()
	return
}
