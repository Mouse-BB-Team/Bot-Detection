package schema

import "time"

type EventType struct {
	tableName struct{} `sql:"dc.events"`
	Id        int64
	Name      string
}

type Event struct {
	tableName   struct{} `sql:"dc.sessions"`
	Id          int64
	XCoordinate int
	YCoordinate int
	EventTime   time.Time
	EventId     int64
	XResolution int
	YResolution int
}

func InitialEmptyEvent() Event {
	return Event{EventTime: time.Time{}}
}