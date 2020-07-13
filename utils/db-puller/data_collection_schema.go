package db_puller

import (
	"time"
)

type User struct {
	tableName struct{} `sql:"dc.users"`
	Id        int64
	Login     string
}

type Event struct {
	tableName struct{} `sql:"dc.events"`
	Id        int64
	Name      string
}

type Session struct {
	tableName   struct{} `sql:"dc.sessions"`
	Id          int64
	XCoordinate int
	YCoordinate int
	EventTime   time.Time
	XResolution int
	YResolution int
}

