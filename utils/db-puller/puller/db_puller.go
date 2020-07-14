package puller

import (
	"db-puller"
	"db-puller/utils"
	"fmt"
	"github.com/go-pg/pg"
	"sync"
	"time"
)

var lock = sync.Mutex{}


func pull(options *pg.Options) map[db_puller.User]*[]*[]db_puller.Session{

	db := pg.Connect(options)
	defer db.Close()

	users := getUsers(db)
	userSequence := make(map[db_puller.User]*[]*[]db_puller.Session)

	for _, user := range users {
		sessions := getSessions(db, user.Id)
		go routine(userSequence, user, splitIntoSequences(sessions, db_puller.Event{Id: 1}, 1.0))
	}

	return userSequence
}

func routine(userSequence map[db_puller.User]*[]*[]db_puller.Session, user db_puller.User, sequence *[]*[]db_puller.Session) {
	lock.Lock()
	defer lock.Unlock()

	userSequence[user] = sequence
}

func getUsers(db *pg.DB) (users []db_puller.User) {
	err := db.Model(&users).Select()
	utils.HandleError(err)
	return
}

func getSessions(db *pg.DB, userId int64) (sessions []db_puller.Session) {
	err := db.Model(&sessions).Where(fmt.Sprintf("%s = ?", UserIdAttribute), userId).Order(fmt.Sprintf("%s ASC", EventTimeAttribute)).Select()
	utils.HandleError(err)
	return
}

func splitIntoSequences(sessions []db_puller.Session, event db_puller.Event, gapSeconds float64) (sequences *[]*[]db_puller.Session) {

	var currSequence = new([]db_puller.Session)

	sequences = new([]*[]db_puller.Session)
	*sequences = append(*sequences, currSequence)

	var prev = db_puller.Session{EventTime: time.Time{}}

	for _, curr := range sessions {
		if curr.EventId == event.Id {
			if isBeginOfNewSequence(prev.EventTime, curr.EventTime, gapSeconds) {
				if isPreviousSequenceToShort(currSequence, 10) {
					*sequences = (*sequences)[:len(*sequences) - 1]
				}
				currSequence = new([]db_puller.Session)
				*sequences = append(*sequences, currSequence)
			}

			*currSequence = append(*currSequence, curr)
			prev = curr
		}
	}
	return
}

func isPreviousSequenceToShort(sequence *[]db_puller.Session, length int) bool{
	return len(*sequence) < length
}

func isBeginOfNewSequence(prev time.Time, curr time.Time, delayGap float64) bool {
	if !prev.IsZero() {
		return curr.Sub(prev).Seconds() > delayGap
	} else {
		return false
	}
}
