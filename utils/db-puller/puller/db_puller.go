package puller

import (
	"db-puller"
	"db-puller/utils"
	"fmt"
	"github.com/go-pg/pg"
	"time"
)

func pull(options *pg.Options) {
	db := pg.Connect(options)
	defer db.Close()

	users := getUsers(db)

	for _, user := range users {
		sessions := getSessions(db, user.Id)
		splitIntoSequences(sessions, db_puller.Event{Id: 1}, 1.0)

	}

	fmt.Println(users)
}

func getUsers(db *pg.DB) (users []db_puller.User) {
	err := db.Model(&users).Select()
	utils.HandleError(err)
	return
}

func getSessions(db *pg.DB, userId int64) (sessions []db_puller.Session) {
	err := db.Model(&sessions).Where("user_id = ?", userId).Order("event_time ASC").Select()
	utils.HandleError(err)
	return
}

func splitIntoSequences(sessions []db_puller.Session, event db_puller.Event, gapSeconds float64) (sequences []*[]db_puller.Session) {

	var currSequence = new([]db_puller.Session)

	sequences = append(sequences, currSequence)

	var prev = db_puller.Session{EventTime: time.Time{}}

	for _, curr := range sessions {
		if curr.EventId == event.Id {
			if isNewSequence(prev.EventTime, curr.EventTime, gapSeconds) {
				currSequence = new([]db_puller.Session)
				sequences = append(sequences, currSequence)
			}

			*currSequence = append(*currSequence, curr)
			prev = curr
		}
	}
	return
}

func isNewSequence(prev time.Time, curr time.Time, delayGap float64) bool {
	if !prev.IsZero() {
		return curr.Sub(prev).Seconds() > delayGap
	} else {
		return false
	}
}
