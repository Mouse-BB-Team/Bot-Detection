package cmd

import (
	"flag"
	"os"
	"path/filepath"
	"serializer/consts"
	"serializer/utils"
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
	OutputPath        *string
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
	args.OutputPath = flag.String("output", getProgramPath(), "program output path")
	flag.Parse()
	return
}

func getProgramPath() string {
	dir, err := filepath.Abs(filepath.Dir(os.Args[0]))
	utils.HandleError(err)
	return dir
}
