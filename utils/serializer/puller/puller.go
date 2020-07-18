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

type Puller struct {
	Options  *pg.Options
	database *pg.DB
}

func (puller *Puller) Connect() {
	puller.database = pg.Connect(puller.Options)
}

func (puller *Puller) Close() {
	utils.HandleError(puller.database.Close())
}

func (puller *Puller) Pull(splitArgs lists.SplitArgs) (*map[schema.User]*lists.SequenceList, int, int) {
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
