package schema

type User struct {
	tableName struct{} `sql:"dc.users"`
	Id        int64
	Login     string
}
