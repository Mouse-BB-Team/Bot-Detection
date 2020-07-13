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
		splitIntoSequences(sessions)

	}

	fmt.Println(users)
}

func getUsers(db *pg.DB) (users []db_puller.User) {
	err := db.Model(&users).Select()
	utils.HandleError(err)
	return
}

func getSessions(db *pg.DB, userId int64) (sessions []db_puller.Session) {
	err := db.Model(&sessions).Where("user_id = ?", userId).Order("ASC event_time").Select()
	utils.HandleError(err)
	return
}

func splitIntoSequences(sessions []db_puller.Session) (sequences []*[]db_puller.Session) {

	var sequenceGapSeconds = 1.0

	//var currSequence *[]db_puller.Session

	var prev db_puller.Session

	for _, element := range sessions {
		if isNewSequence(prev.EventTime, element.EventTime, sequenceGapSeconds) {

		}

		//currSequence
	}
	return nil
}

func isNewSequence(prev time.Time, curr time.Time, delayGap float64) bool {
	return curr.Sub(prev).Seconds() > delayGap
}
