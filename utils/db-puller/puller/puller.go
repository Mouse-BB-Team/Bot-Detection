package puller

import (
	"db-puller/puller/schema/event"
	"db-puller/puller/schema/user"
	"db-puller/puller/sequences"
	"db-puller/utils"
	"fmt"
	"github.com/go-pg/pg"
)

var whereArgument = fmt.Sprintf("%s = ?", UserIdAttribute)
var orderArgument = fmt.Sprintf("%s ASC", EventTimeAttribute)

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

func (puller *Puller) Pull(eventType event.EventType, gapDelay float64, minSequenceLength int) map[user.User]*sequences.SequenceList {
	users := getUsersFrom(puller.database)
	sequenceList := make(map[user.User]*sequences.SequenceList)

	for _, usr := range users {
		sessions := getSessionsFor(usr, puller.database)
		sequenceList[usr] = sessions.Split(eventType, gapDelay, minSequenceLength)
	}

	return sequenceList
}

func getUsersFrom(db *pg.DB) (users []user.User) {
	err := db.Model(&users).Select()
	utils.HandleError(err)
	return
}

func getSessionsFor(user user.User, db *pg.DB) (sessions sequences.Sequence) {
	var events []event.Event
	err := db.Model(&events).Where(whereArgument, user.Id).Order(orderArgument).Select()
	utils.HandleError(err)
	sessions.Set(events)
	return
}

