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
}

func ParseArgs() (args Args) {
	args.GapTime = flag.Float64("gap-delay", 1.0, "gap between lists")
	args.MinSequenceLength = flag.Int("min-seq-length", 10, "minimal sequence length")
	args.InfoRequired = flag.Bool("info", false, "if print info message")
	args.DBPort = flag.Int("db-port", consts.DefaultDatabasePort, "database port")
	args.DBName = flag.String("db-name", consts.DefaultDatabaseName, "database name")
	args.DBUser = flag.String("db-user", consts.DefaultDatabaseUser, "database user")
	args.DBPassword = flag.String("db-password", consts.DefaultDatabasePassword, "database password")
	args.EventTypeId = flag.Int("event-type", consts.DefaultEventTypeId, "event type id")
	flag.Parse()
	return
}
