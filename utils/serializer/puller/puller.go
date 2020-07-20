package puller

import (
	"fmt"
	"github.com/Mouse-BB-Team/Bot-Detection/utils/serializer/consts"
	"github.com/Mouse-BB-Team/Bot-Detection/utils/serializer/lists"
	"github.com/Mouse-BB-Team/Bot-Detection/utils/serializer/schema"
	"github.com/Mouse-BB-Team/Bot-Detection/utils/serializer/utils"
	"github.com/go-pg/pg"
)

var whereArgument = fmt.Sprintf("%s = ?", consts.UserIdAttribute)
var orderArgument = fmt.Sprintf("%s ASC", consts.EventTimeAttribute)

type Puller interface {
	Connect()
	Close()
	Pull(args lists.SplitArgs) (*map[schema.User]*lists.SequenceList, int, int)
	getDatabase() *pg.DB
}

type DBPuller struct {
	Options  *pg.Options
	database *pg.DB
}

func NewDBPuller(options *pg.Options) Puller {
	return &DBPuller{Options: options}
}

func (puller *DBPuller) Connect() {
	puller.database = pg.Connect(puller.Options)
}

func (puller *DBPuller) Close() {
	utils.HandleError(puller.database.Close())
}

func (puller *DBPuller) Pull(splitArgs lists.SplitArgs) (*map[schema.User]*lists.SequenceList, int, int) {
	users := getUsersFrom(puller.database)
	sequenceList := make(map[schema.User]*lists.SequenceList)

	for _, usr := range users {
		pullForUser(usr, splitArgs, puller, &sequenceList)
	}

	return &sequenceList, countUsers(&sequenceList), countSequences(&sequenceList)
}

func (puller *DBPuller) getDatabase() *pg.DB{
	return puller.database
}

type OneUserDBPuller struct {
	dbPuller *DBPuller
	userId   int
}

func NewDBPullerForOneUser(options *pg.Options, userId int) Puller {
	dbPuller := &DBPuller{Options: options}
	return &OneUserDBPuller{dbPuller: dbPuller}
}

func (puller *OneUserDBPuller) Connect() {
	puller.dbPuller.database = pg.Connect(puller.dbPuller.Options)
}

func (puller *OneUserDBPuller) Close() {
	utils.HandleError(puller.dbPuller.database.Close())
}

func (puller *OneUserDBPuller) Pull(splitArgs lists.SplitArgs) (*map[schema.User]*lists.SequenceList, int, int) {
	sequenceList := make(map[schema.User]*lists.SequenceList)

	usr := schema.User{Id: int64(puller.userId)}

	pullForUser(usr, splitArgs, puller, &sequenceList)

	return &sequenceList, 1, countSequences(&sequenceList)
}

func (puller *OneUserDBPuller) getDatabase() *pg.DB {
	return puller.dbPuller.database
}

func pullForUser(user schema.User, splitArgs lists.SplitArgs, puller Puller, sequenceList *map[schema.User]*lists.SequenceList) {
	sessions := getSessionsFor(user, puller.getDatabase())

	result := sessions.Split(splitArgs)

	if result.Get() != nil {
		(*sequenceList)[user] = result
	}
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
