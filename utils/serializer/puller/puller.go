package puller

import (
	"fmt"
	"github.com/go-pg/pg"
	"serializer/consts"
	"serializer/lists"
	"serializer/schema"
	"serializer/utils"
)

var whereArgument = fmt.Sprintf("%s = ?", consts.UserIdAttribute)
var orderArgument = fmt.Sprintf("%s ASC", consts.EventTimeAttribute)

type Puller interface {
	Connect()
	Close()
	Pull(args lists.SplitArgs) (*map[schema.User]*lists.SequenceList, int, int)
}

type DBPuller struct {
	Options  *pg.Options
	database *pg.DB
}

type OneUserDBPuller struct {
	dbPuller *DBPuller
	userId   int
}

func NewDBPuller(options *pg.Options) Puller {
	return &DBPuller{Options: options}
}

func NewDBPullerForOneUser(options *pg.Options, userId int) Puller {
	dbPuller := &DBPuller{Options: options}
	return &OneUserDBPuller{dbPuller: dbPuller}
}

func (puller *OneUserDBPuller) Connect() {
	puller.dbPuller.database = pg.Connect(puller.dbPuller.Options)
}

func (puller *DBPuller) Connect() {
	puller.database = pg.Connect(puller.Options)
}

func (puller *OneUserDBPuller) Close() {
	utils.HandleError(puller.dbPuller.database.Close())
}

func (puller *DBPuller) Close() {
	utils.HandleError(puller.database.Close())
}

func (puller *OneUserDBPuller) Pull(splitArgs lists.SplitArgs) (*map[schema.User]*lists.SequenceList, int, int) {
	sequenceList := make(map[schema.User]*lists.SequenceList)

	usr := schema.User{Id: int64(puller.userId)}

	sessions := getSessionsFor(usr, puller.dbPuller.database)

	result := sessions.Split(splitArgs)

	if result.Get() != nil {
		sequenceList[usr] = result
	}

	return &sequenceList, 1, countSequences(&sequenceList)
}

func (puller *DBPuller) Pull(splitArgs lists.SplitArgs) (*map[schema.User]*lists.SequenceList, int, int) {
	users := getUsersFrom(puller.database)
	sequenceList := make(map[schema.User]*lists.SequenceList)

	for _, usr := range users {
		sessions := getSessionsFor(usr, puller.database)

		result := sessions.Split(splitArgs)

		if result.Get() != nil {
			sequenceList[usr] = result
		}
	}

	return &sequenceList, countUsers(&sequenceList), countSequences(&sequenceList)
}

func getUsersFrom(db *pg.DB) (users []schema.User) {
	err := db.Model(&users).Select()
	utils.HandleError(err)
	return
}

func getSessionsFor(user schema.User, db *pg.DB) (sessions lists.EventList) {
	var events []schema.Event
	err := db.Model(&events).Where(whereArgument, user.Id).Order(orderArgument).Select()
	utils.HandleError(err)
	sessions.Set(events)
	return
}

func countUsers(result *map[schema.User]*lists.SequenceList) int {
	return len(*result)
}

func countSequences(result *map[schema.User]*lists.SequenceList) int {
	count := 0

	for _, v := range *result {
		count += len(v.Get())
	}

	return count
}
