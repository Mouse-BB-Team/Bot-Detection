package puller

import (
	"github.com/go-pg/pg"
	"testing"
)

func TestPull(t *testing.T) {
	pull(&pg.Options{
		Addr:     ":5432",
		User:     "admin",
		Password: "admin",
		Database: "data_collection",
	})
}
